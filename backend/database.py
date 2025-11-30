# backend/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 📌 Carrega .env da pasta backend APENAS se existir
# (Docker sempre usa variáveis de ambiente externas)
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# 🔄 Docker ou o sistema operacional podem sobrescrever
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ Erro: DATABASE_URL não encontrada no ambiente ou backend/.env")

# 🚀 Engine pronto para SQLAlchemy 2.x e Docker
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # evita conexões quebradas
    future=True           # compatível com SQLAlchemy 2.x
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

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
