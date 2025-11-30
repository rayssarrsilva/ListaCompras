import sys
import os

# Ajuste de path (não prejudica no Docker, mas mantém compatibilidade local)
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Base
from database import engine
from routes.auth import router as auth_router
from routes.carts import router as cart_router

app = FastAPI(title="Lista de Compras API")

# CORS aberto para funcionar no Docker, local e deploy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # facilitar desenvolvimento + containers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚫 REMOVIDO: create_all (não desejável em produção/Docker)
# Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(cart_router)

@app.get("/")
def root():
    return {"message": "API ListaCompras está rodando 🚀"}
