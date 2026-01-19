from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from coordinator.client import execute_command

app = FastAPI(title="Calculator Distribuit")

app.mount("/static", StaticFiles(directory="static"), name="static")

class CalcRequest(BaseModel):
    command: str

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/calc")
def calc(req: CalcRequest):
    return execute_command(req.command)
