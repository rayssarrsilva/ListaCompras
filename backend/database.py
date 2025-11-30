# backend/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 🔑 Carrega o .env da pasta backend/
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# 🔄 Permite que DOCKER ou o sistema operacional sobrescreva o valor
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ Erro: DATABASE_URL não encontrada no ambiente ou backend/.env")

# 🚀 engine agora suporta docker sem mudar nada para local
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # evita conexões quebradas no Docker
    future=True           # compatível com SQLAlchemy 2.x
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"❌ Erro na sessão do banco: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()
