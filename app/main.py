from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from app.crud import create_task, get_task, update_task, delete_task, get_all_tasks
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate 
from typing import List
app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost",  # Permitir tu frontend en localhost
    "http://localhost:3000",  # Permitir frontend en puerto 3000 (React, Vite, etc)
    "http://127.0.0.1:8000",
    "https://tudominio.com",  # Permitir tu dominio en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permitir todos los headers
)

@app.get("/tasks/", response_model=List[Task])
async def list_tasks():
    tasks = await get_all_tasks()
    return tasks

@app.post("/tasks/", response_model=Task)
async def create(task: TaskCreate):
    created_task = await create_task(task)
    if not created_task:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return created_task 

@app.get("/tasks/{task_id}", response_model=Task)
async def read(task_id: str):
    task = await get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update(task_id: str, task: TaskUpdate):
    updated_task = await update_task(task_id, task.dict(exclude_unset=True))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task  # Retorna el objeto `Task` completo actualizado

@app.delete("/tasks/{task_id}")
async def delete(task_id: str):
    success = await delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}