import json
import os
from typing import List, Dict

import tempfile

DATA_FILE = os.path.join(tempfile.gettempdir(), "mindstep_data.json")

class MindStepManager:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.tasks = self._load_data()

    def _load_data(self) -> List[Dict]:
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)

    def create_task(self, title: str, micro_steps: List[str]):
        """Cria uma tarefa se tiver ao menos 3 micro-passos."""
        if not title.strip():
            raise ValueError("A tarefa precisa ter um título.")
            
        if len(micro_steps) < 3:
            raise ValueError("Paralisia de análise: Por favor, quebre esta tarefa em pelo menos 3 micro-passos menores para começar.")

        new_task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "completed": False,
            "steps": [{"name": step, "completed": False} for step in micro_steps]
        }
        self.tasks.append(new_task)
        self._save_data()
        return new_task

    def complete_micro_step(self, task_id: int, step_index: int):
        """Marca um micro-passo como concluído e checa se a tarefa principal acabou."""
        for task in self.tasks:
            if task["id"] == task_id:
                if step_index < 0 or step_index >= len(task["steps"]):
                    raise IndexError("Micro-passo não encontrado.")
                
                task["steps"][step_index]["completed"] = True
                
                # Checa se todos estão concluídos
                all_completed = all(step["completed"] for step in task["steps"])
                if all_completed:
                    task["completed"] = True
                    
                self._save_data()
                return task
        raise KeyError(f"Tarefa {task_id} não encontrada.")

    def get_all_tasks(self):
        return self.tasks
