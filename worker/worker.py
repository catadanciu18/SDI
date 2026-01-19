import socket, sys, math
from functools import reduce

PORT = int(sys.argv[1])

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", PORT))
s.listen(5)

print(f"Worker {PORT} pornit", flush=True)

def handle(op, nums):
    if op == "sum":
        return sum(nums)
    if op == "prod":
        return math.prod(nums)
    if op == "min":
        return min(nums)
    if op == "max":
        return max(nums)
    if op == "avg":
        return f"{sum(nums)}|{len(nums)}"
    if op == "pow":
        return pow(nums[0], nums[1])
    if op == "fact":
        return math.factorial(nums[0])
    if op in ("cmmdc", "gcd"):
        return reduce(math.gcd, nums)
    if op in ("cmmmc", "lcm"):
        return reduce(lambda a, b: a * b // math.gcd(a, b), nums)
    return "ERR operatie necunoscuta"

while True:
    conn, _ = s.accept()
    data = conn.recv(4096).decode().strip()

    try:
        parts = data.split()
        op = parts[0]
        nums = list(map(int, parts[1:]))
        result = handle(op, nums)
        conn.sendall(str(result).encode())
    except Exception as e:
        conn.sendall(f"ERR {e}".encode())

    conn.close()
