# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import Base          # ← Importa Base do models.py (na mesma pasta)
from .database import engine      # ← Importa engine do database.py (na mesma pasta)
from .routes.auth import router as auth_router
from .routes.carts import router as cart_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lista de Compras API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(cart_router)

@app.get("/")
def root():
    return {"message": "API ListaCompras está rodando 🚀"}