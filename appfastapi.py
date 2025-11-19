from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_routes import router as cart_router
from fastapi_auth_routes import router as auth_router
from database import engine
from models import db

app = FastAPI(title="Lista de Compras API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db.metadata.create_all(bind=engine)

# Inclui rotas
app.include_router(auth_router)
app.include_router(cart_router)

@app.get("/")
def root():
    return {"message": "API ListaCompras está rodando 🚀"}
