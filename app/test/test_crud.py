import pytest
from app.crud import create_task, get_task, update_task, delete_task
from app.models import Task
from app.database import tasks_collection
from bson import ObjectId

@pytest.mark.asyncio
async def test_create_task():
    new_task = Task(
        title="Tarea de prueba",
        description="Esta es una tarea de prueba, primera tarea",
        status="to_do"
    )
    task_id = await create_task(new_task)
    assert isinstance(task_id, str)

@pytest.mark.asyncio
async def test_get_task():
    # Crear un nuevo objeto Task
    new_task = Task(
        title="Crear backend",
        description="Esta es una tarea de prueba",
        status="to_do"
    )
    
    # Insertar la tarea en la base de datos usando la función 'create_task'
    task_id = await create_task(new_task)
    
    # Obtener la tarea recién creada usando la función 'get_task'
    task = await get_task(task_id)
    
    # Validar que se recuperó correctamente y tiene el título esperado
    assert task is not None  # Verificamos que la tarea se haya encontrado
    assert task.title == "Crear backend"  # Verificamos que el título coincida
    assert task.description == "Esta es una tarea de prueba"
    assert task.status == "to_do"


@pytest.mark.asyncio
async def test_update_task():
    new_task = Task(
        title="Crear forntend",
        description="Esta es una tarea de prueba",
        status="to_do"
    )
    task_id = await create_task(new_task)
    updated_task = await update_task(task_id, {"status": "completed"})
    assert updated_task.status == "completed"

@pytest.mark.asyncio
async def test_delete_task():
    new_task = Task(
        title="Dockerizar la solucion",
        description="Esta es una tarea de prueba",
        status="to_do"
    )
    task_id = await create_task(new_task)
    result = await delete_task(task_id)
    assert result is True