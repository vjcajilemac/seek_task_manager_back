from app.models import Task
from app.database import tasks_collection
from bson import ObjectId
from typing import Union, List

async def get_all_tasks() -> List[Task]:
    tasks = []
    async for task in tasks_collection.find():
        task["id"] = str(task["_id"])  # Convertimos `_id` a `id`
        del task["_id"]  # Eliminamos `_id` para que no se incluya en la respuesta
        tasks.append(Task(**task))
    return tasks

async def create_task(task: Task) -> Union[dict, None]:
    task_dict = task.dict(by_alias=True, exclude_unset=True)
    
    # 🔍 Insertamos el documento en la base de datos
    result = await tasks_collection.insert_one(task_dict)
    created_id = result.inserted_id  # Obtenemos el ID del documento creado
    
    # 🔍 Consultamos el documento recién creado para devolverlo completo
    created_task = await tasks_collection.find_one({"_id": created_id})
    
    if created_task:
        created_task["id"] = str(created_task["_id"])  # Convertimos `_id` a `id`
        del created_task["_id"]  # Eliminamos `_id` porque FastAPI no lo permite
        return created_task  # 🔍 Devolvemos un diccionario, NO un objeto Task
    
    return None

async def get_task(task_id: str) -> Union[Task, None]:
    task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    if task:
        task["id"] = str(task["_id"])  # Convertimos `_id` a `id`
        del task["_id"]  # Eliminamos `_id` para que no sea devuelto nunca
        return Task(**task)
    return None

async def update_task(task_id: str, task_data: dict) -> Union[Task, None]:
    if "_id" in task_data:
        del task_data["_id"]  # Eliminamos `_id` para evitar conflicto

    task_data = {k: v for k, v in task_data.items() if v is not None}  # Filtramos campos `None`

    if not task_data:
        return await get_task(task_id)

    await tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": task_data})
    return await get_task(task_id)  # Devolvemos el Task actualizado con `id` en lugar de `_id`

async def delete_task(task_id: str):
    result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count > 0