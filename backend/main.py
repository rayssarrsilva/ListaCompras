# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import Base
from .database import engine

# Cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lista de Compras API")

# 🔑 CONFIGURAÇÃO CORS INFALÍVEL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],  # URL do seu frontend Flask
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importa e inclui rotas APENAS após o CORS
from .routes.auth import router as auth_router
from .routes.carts import router as cart_router

app.include_router(auth_router)
app.include_router(cart_router)

@app.get("/")
def root():
    return {"message": "API ListaCompras está rodando 🚀"}