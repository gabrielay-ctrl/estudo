"""
MindStep Web — Arquivo único auto-contido para deploy na Vercel.
Toda a lógica (API client, gerenciador de tarefas, HTML) vive aqui dentro.
"""

# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Request
# pyrefly: ignore [missing-import]
from fastapi.responses import HTMLResponse, JSONResponse
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import List, Dict
import requests
import tempfile
import json
import os

# ──────────────────────────────────────────────
# 1. API Client — Consome a API pública AdviceSlip
# ──────────────────────────────────────────────

def get_motivational_advice() -> str:
    """Busca um conselho motivacional da API pública AdviceSlip."""
    try:
        response = requests.get("https://api.adviceslip.com/advice", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["slip"]["advice"]
    except Exception:
        pass
    return "Lembre-se: avance 1% de cada vez. Beba água!"

# ──────────────────────────────────────────────
# 2. Gerenciador de Tarefas (MindStepManager)
# ──────────────────────────────────────────────

DATA_FILE = os.path.join(tempfile.gettempdir(), "mindstep_data.json")


class MindStepManager:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.tasks = self._load_data()

    def _load_data(self) -> List[Dict]:
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)

    def create_task(self, title: str, micro_steps: List[str]):
        """Cria uma tarefa se tiver ao menos 3 micro-passos."""
        if not title.strip():
            raise ValueError("A tarefa precisa ter um título.")
        if len(micro_steps) < 3:
            raise ValueError(
                "Paralisia de análise: Por favor, quebre esta tarefa "
                "em pelo menos 3 micro-passos menores para começar."
            )
        new_task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "completed": False,
            "steps": [{"name": step, "completed": False} for step in micro_steps],
        }
        self.tasks.append(new_task)
        self._save_data()
        return new_task

    def complete_micro_step(self, task_id: int, step_index: int):
        """Marca um micro-passo como concluído."""
        for task in self.tasks:
            if task["id"] == task_id:
                if step_index < 0 or step_index >= len(task["steps"]):
                    raise IndexError("Micro-passo não encontrado.")
                task["steps"][step_index]["completed"] = True
                if all(step["completed"] for step in task["steps"]):
                    task["completed"] = True
                self._save_data()
                return task
        raise KeyError(f"Tarefa {task_id} não encontrada.")

    def get_all_tasks(self):
        return self.tasks


# ──────────────────────────────────────────────
# 3. FastAPI — Rotas
# ──────────────────────────────────────────────

app = FastAPI(title="MindStep Web")
manager = MindStepManager()


class TaskCreate(BaseModel):
    title: str
    steps: List[str]


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    advice = get_motivational_advice()
    tasks = manager.get_all_tasks()

    # Gera as cards de tarefas dinamicamente
    tasks_html = ""
    if not tasks:
        tasks_html = """
        <div style="text-align:center; color:var(--text-muted); padding:2rem;">
            Nenhuma tarefa ainda. Crie sua primeira tarefa acima!
        </div>"""
    else:
        for task in tasks:
            badge = ""
            if task["completed"]:
                badge = '<span class="status-badge">Concluída! 🎉</span>'

            steps_html = ""
            for i, step in enumerate(task["steps"]):
                css_class = "micro-step completed" if step["completed"] else "micro-step"
                onclick = "" if step["completed"] else f'onclick="completeStep({task["id"]}, {i})"'
                check = "✓" if step["completed"] else ""
                steps_html += f'''
                <div class="{css_class}" {onclick}>
                    <div class="checkbox">{check}</div>
                    <span>{step["name"]}</span>
                </div>'''

            tasks_html += f'''
            <div class="task-item">
                <div class="task-header">
                    <span class="task-title">{task["title"]}</span>
                    {badge}
                </div>
                <div class="steps-list">{steps_html}</div>
            </div>'''

    # ──────────────────────────────────────────
    # 4. HTML + CSS + JS — Tudo inline
    # ──────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MindStep - Avance 1% ao Dia</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --primary: #8b5cf6;
            --primary-hover: #7c3aed;
            --success: #10b981;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
        body {{
            background-color: var(--bg-color);
            background-image:
                radial-gradient(circle at top right, rgba(139,92,246,0.15), transparent 40%),
                radial-gradient(circle at bottom left, rgba(16,185,129,0.1), transparent 40%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 2rem;
            display: flex; flex-direction: column; align-items: center;
        }}
        .container {{ max-width: 800px; width: 100%; margin-top: 2rem; }}
        header {{ text-align: center; margin-bottom: 3rem; }}
        h1 {{
            font-size: 3rem; font-weight: 800;
            background: linear-gradient(to right, #a78bfa, #34d399);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 1rem; animation: fadeInDown 0.8s ease-out;
        }}
        .advice-card {{
            background: var(--card-bg); backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.1); border-radius: 16px;
            padding: 1.5rem; text-align: center; margin-bottom: 3rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2); animation: fadeIn 1s ease-out;
        }}
        .advice-card p {{ font-size: 1.2rem; font-weight: 300; font-style: italic; color: #e2e8f0; }}
        .advice-badge {{
            display: inline-block; background: rgba(139,92,246,0.2); color: #c4b5fd;
            padding: 0.2rem 0.8rem; border-radius: 99px; font-size: 0.8rem;
            margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;
        }}
        .task-creation {{
            background: var(--card-bg); backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.1); border-radius: 16px;
            padding: 2rem; margin-bottom: 2rem;
        }}
        .input-group {{ margin-bottom: 1.5rem; }}
        label {{ display: block; margin-bottom: 0.5rem; color: var(--text-muted); font-weight: 600; }}
        input[type="text"] {{
            width: 100%; padding: 1rem;
            background: rgba(15,23,42,0.6); border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px; color: white; font-size: 1rem; transition: all 0.3s ease;
        }}
        input[type="text"]:focus {{
            outline: none; border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(139,92,246,0.3);
        }}
        .step-container {{ display: flex; flex-direction: column; gap: 0.5rem; }}
        button {{
            background: var(--primary); color: white; border: none;
            padding: 1rem 2rem; border-radius: 8px; font-size: 1rem;
            font-weight: 600; cursor: pointer; width: 100%;
            transition: background 0.3s ease, transform 0.1s ease;
        }}
        button:hover {{ background: var(--primary-hover); }}
        button:active {{ transform: scale(0.98); }}
        .tasks-list {{ display: flex; flex-direction: column; gap: 1.5rem; }}
        .task-item {{
            background: var(--card-bg); border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px; padding: 1.5rem; transition: transform 0.2s ease;
        }}
        .task-item:hover {{ transform: translateY(-2px); border-color: rgba(255,255,255,0.2); }}
        .task-header {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 1rem;
        }}
        .task-title {{ font-size: 1.4rem; font-weight: 600; }}
        .status-badge {{
            background: rgba(16,185,129,0.2); color: #34d399;
            padding: 0.3rem 0.8rem; border-radius: 99px; font-size: 0.8rem; font-weight: 600;
        }}
        .micro-step {{
            display: flex; align-items: center; padding: 0.8rem;
            background: rgba(15,23,42,0.4); border-radius: 8px;
            margin-bottom: 0.5rem; cursor: pointer; transition: all 0.2s;
        }}
        .micro-step:hover {{ background: rgba(15,23,42,0.8); }}
        .micro-step.completed {{ opacity: 0.6; text-decoration: line-through; }}
        .checkbox {{
            width: 20px; height: 20px; border: 2px solid var(--primary);
            border-radius: 4px; margin-right: 1rem;
            display: flex; align-items: center; justify-content: center;
            font-size: 14px; color: white;
        }}
        .completed .checkbox {{ background: var(--primary); border-color: var(--primary); }}
        #error-msg {{ color: #ef4444; margin-top: 1rem; font-size: 0.9rem; display: none; }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>MindStep</h1>
            <p style="color:var(--text-muted);">Quebre a paralisia. Avance 1% ao dia.</p>
        </header>

        <div class="advice-card">
            <span class="advice-badge">Conselho do Dia (API)</span>
            <p>"{advice}"</p>
        </div>

        <div class="task-creation">
            <h2 style="margin-bottom:1.5rem; font-size:1.2rem;">Nova Tarefa</h2>
            <div class="input-group">
                <label>Objetivo Principal</label>
                <input type="text" id="task-title" placeholder="Ex: Arrumar o quarto">
            </div>
            <div class="input-group">
                <label>Micro-passos (mínimo 3)</label>
                <div class="step-container">
                    <input type="text" class="step-input" placeholder="Passo 1 (Ex: Levantar da cama)">
                    <input type="text" class="step-input" placeholder="Passo 2 (Ex: Pegar um saco de lixo)">
                    <input type="text" class="step-input" placeholder="Passo 3 (Ex: Jogar fora 1 papel)">
                </div>
            </div>
            <button onclick="createTask()">Começar a Jornada</button>
            <div id="error-msg"></div>
        </div>

        <div class="tasks-list">
            {tasks_html}
        </div>
    </div>

    <script>
        async function createTask() {{
            const title = document.getElementById('task-title').value;
            const stepInputs = document.querySelectorAll('.step-input');
            const errorMsg = document.getElementById('error-msg');
            const steps = Array.from(stepInputs).map(i => i.value.trim()).filter(v => v !== '');
            try {{
                const r = await fetch('/api/tasks', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{ title, steps }})
                }});
                const data = await r.json();
                if (data.status === 'success') {{ window.location.reload(); }}
                else {{ errorMsg.textContent = data.message; errorMsg.style.display = 'block'; }}
            }} catch (err) {{ console.error(err); }}
        }}
        async function completeStep(taskId, stepIndex) {{
            try {{
                const r = await fetch(`/api/tasks/${{taskId}}/steps/${{stepIndex}}`, {{ method: 'POST' }});
                const data = await r.json();
                if (data.status === 'success') {{ window.location.reload(); }}
            }} catch (err) {{ console.error(err); }}
        }}
    </script>
</body>
</html>"""
    return HTMLResponse(content=html)


@app.post("/api/tasks")
async def create_task(task: TaskCreate):
    try:
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
