# todo_list.py
import json
import os
from dataclasses import dataclass, asdict

TASKS_FILE = 'tasks.json'


@dataclass
class Task:
    id: int
    title: str
    description: str
    due_date: str
    status: str = 'Pending'
    priority: str = 'Medium'


class ToDoListManager:
    def __init__(self, storage_file=TASKS_FILE):
        self.storage_file = storage_file
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                self.tasks = [Task(**t) for t in data]
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.storage_file, 'w') as f:
            json.dump([asdict(t) for t in self.tasks], f, indent=2)

    def add_task(self, title, description, due_date, priority='Medium'):
        next_id = max((t.id for t in self.tasks), default=0) + 1
        task = Task(next_id, title, description, due_date, priority=priority)
        self.tasks.append(task)
        self.save_tasks()
        return task

    def list_tasks(self):
        if not self.tasks:
            print('No hay tareas.')
            return
        print('Tareas:')
        for t in self.tasks:
            print(
                f'{t.id}. {t.title} [{t.status}] - '
                f'Vence: {t.due_date} - Prioridad: {t.priority}'
            )

    def mark_completed(self, task_id):
        for t in self.tasks:
            if t.id == task_id:
                t.status = 'Completed'
                self.save_tasks()
                return
        print(f'No existe tarea con ID {task_id}.')

    def clear_tasks(self):
        self.tasks = []
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)

    # ---- MÉTODOS NUEVOS ----
    def remove_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save_tasks()

    def edit_task(self, task_id, **kwargs):
        for t in self.tasks:
            if t.id == task_id:
                for k, v in kwargs.items():
                    if hasattr(t, k):
                        setattr(t, k, v)
                self.save_tasks()
                return
        print(f'No existe tarea con ID {task_id}.')
