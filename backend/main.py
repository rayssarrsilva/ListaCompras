import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Base
from database import engine
from routes.auth import router as auth_router
from routes.carts import router as cart_router

# ✅ CRIA AS TABELAS NO BANCO (se não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lista de Compras API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(cart_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API ListaCompras está rodando 🚀"}