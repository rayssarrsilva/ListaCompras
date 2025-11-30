# backend/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models import User
from database import get_db
from security import create_access_token

router = APIRouter(tags=["Auth"])

class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    # 🔎 Diagnóstico (temporário)
    print("✅ ENGINE USADA NA ROTA:", db.bind.url)

    if db.query(User).filter_by(username=user_data.username).first():
        print(f"❌ Usuário já existe: {user_data.username}")
        raise HTTPException(status_code=400, detail="Nome de usuário já existe")

    try:
        new_user = User(username=user_data.username)
        new_user.set_password(user_data.password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print(f"✅ Usuário criado com ID {new_user.id}: {new_user.username}")
        return {"message": "Conta criada com sucesso"}

    except Exception as e:
        print(f"❌ Erro inesperado ao registrar: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    print(f"🔍 Tentando login: {user_data.username}")
    try:
        user = db.query(User).filter_by(username=user_data.username).first()

        if not user:
            print(f"❌ Usuário não encontrado: {user_data.username}")
            raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

        if not user.check_password(user_data.password):
            print(f"❌ Senha incorreta para: {user_data.username}")
            raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

        # ✅ Corrigido: o token deve receber data={"sub": id}
        token = create_access_token(user.id)  # ← só o ID inteiro

        print(f"✅ Login bem-sucedido para: {user.username} (ID: {user.id})")
        return {"access_token": token, "token_type": 'bearer'}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro inesperado no login: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
