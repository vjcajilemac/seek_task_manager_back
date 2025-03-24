from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tasks, auth  # Importamos las rutas agrupadas

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "https://tudominio.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Incluir las rutas agrupadas
app.include_router(auth.router)   # Rutas relacionadas a Autenticación
app.include_router(tasks.router)  # Rutas relacionadas a Tareas (Protegidas)