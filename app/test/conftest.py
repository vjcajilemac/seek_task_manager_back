import pytest
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    """
    Crear un nuevo bucle de eventos para cada sesión de prueba.
    Este fixture se asegura de que el bucle de eventos no se cierre antes de tiempo.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()