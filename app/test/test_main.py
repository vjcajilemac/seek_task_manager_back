import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app

client = TestClient(app)  # Seguimos usando TestClient para inicializar la app

@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.post(
            "/tasks/",
            json={"title": "Nueva Tarea", "description": "Prueba de tarea", "status": "to_do"}
        )
    assert response.status_code == 200
    assert "task_id" in response.json()

@pytest.mark.asyncio
async def test_get_nonexistent_task():
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.get("/tasks/invalid_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}