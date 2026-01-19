import socket, threading, math

WORKERS = [8001, 8002, 8003]
DISTRIBUTABLE = {"sum", "prod", "min", "max", "avg"}

def call_worker(port, msg, results, idx):
    try:
        s = socket.socket()
        s.connect(("localhost", port))
        s.sendall(msg.encode())

        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk

        s.close()
        results[idx] = data.decode().strip()
    except:
        results[idx] = None

def execute_command(cmd: str):
    parts = cmd.split()
    op = parts[0]
    nums = list(map(int, parts[1:]))

    details = []


    if op in DISTRIBUTABLE:
        chunks = [nums[i::3] for i in range(3)]
        results = [None, None, None]
        threads = []

        for i in range(3):
            if not chunks[i]:
                continue
            msg = op + " " + " ".join(map(str, chunks[i]))
            t = threading.Thread(
                target=call_worker,
                args=(WORKERS[i], msg, results, i)
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        if op == "avg":
            total_sum = 0
            total_count = 0

            for i, r in enumerate(results):
                if r and "|" in r:
                    s, c = r.split("|")
                    total_sum += int(s)
                    total_count += int(c)
                    details.append(
                        f"Worker {WORKERS[i]}: sum={s}, count={c}"
                    )

            return {
                "final": str(total_sum / total_count),
                "details": details
            }

        values = []
        for i, r in enumerate(results):
            if r and not r.startswith("ERR"):
                values.append(int(r))
                details.append(
                    f"Worker {WORKERS[i]}: {op} {chunks[i]} = {r}"
                )

        if op == "sum":
            final = sum(values)
        elif op == "prod":
            final = math.prod(values)
        elif op == "min":
            final = min(values)
        elif op == "max":
            final = max(values)

        return {"final": str(final), "details": details}

    results = [None]
    call_worker(WORKERS[0], cmd, results, 0)

    return {
        "final": results[0],
        "details": [f"Worker {WORKERS[0]} a executat operația"]
    }
