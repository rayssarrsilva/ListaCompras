from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..models import User
from ..database import get_db
from ..security import create_access_token

router = APIRouter(prefix="/api", tags=["Auth"])

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=user_data.username).first():
        raise HTTPException(status_code=400, detail="Nome de usuário já existe")
    new_user = User(username=user_data.username)
    new_user.set_password(user_data.password)
    db.add(new_user)
    db.commit()
    return {"message": "Conta criada com sucesso"}

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=user_data.username).first()
    if not user or not user.check_password(user_data.password):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}