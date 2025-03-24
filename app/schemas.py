from pydantic import BaseModel, Field
from typing import Optional

# 🔍 Request para CREAR tareas
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    
# 🔍 Request para ACTUALIZAR tareas
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    status: Optional[str] = Field(None, pattern="^(to_do|in_progress|completed)$")  # Cambiado a pattern