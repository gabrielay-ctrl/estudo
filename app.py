from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

from src.microstep import MindStepManager
from src.api_client import get_motivational_advice

import os

app = FastAPI(title="MindStep Web")
manager = MindStepManager()

# Corrige o caminho para a Vercel encontrar a pasta templates
base_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

class TaskCreate(BaseModel):
    title: str
    steps: List[str]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Consome a API pública para exibir na tela principal
    advice = get_motivational_advice()
    tasks = manager.get_all_tasks()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "advice": advice, "tasks": tasks}
    )

@app.post("/api/tasks")
async def create_task(task: TaskCreate):
    try:
        # A regra de negócio exige pelo menos 3 passos, o manager cuida disso.
        new_task = manager.create_task(task.title, task.steps)
        return {"status": "success", "task": new_task}
    except ValueError as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/tasks/{task_id}/steps/{step_index}")
async def complete_step(task_id: int, step_index: int):
    try:
        updated_task = manager.complete_micro_step(task_id, step_index)
        return {"status": "success", "task": updated_task}
    except (KeyError, IndexError) as e:
        return {"status": "error", "message": str(e)}
