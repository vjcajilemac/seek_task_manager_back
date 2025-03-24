from fastapi import APIRouter, Depends, HTTPException
from app.crud import create_task, get_task, update_task, get_all_tasks
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from app.dependencies import get_current_user
from typing import List

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)],  # 🔒 Protegemos todas las rutas con JWT
)

@router.get("/", response_model=List[Task])
async def list_tasks():
    return await get_all_tasks()

@router.post("/", response_model=Task)
async def create_task_route(task: TaskCreate):
    return await create_task(task)

@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: str):
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task_route(task_id: str, task: TaskUpdate):
    updated_task = await update_task(task_id, task.dict(exclude_unset=True))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task