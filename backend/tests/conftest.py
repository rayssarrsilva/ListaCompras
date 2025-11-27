import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base
from backend.database import get_db, engine
from backend.main import app as fastapi_app
from fastapi.testclient import TestClient

# --- Configurações para banco de teste ---
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:123@localhost:5432/listacompras_test")

engine_test = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Cria todas as tabelas no banco de teste
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield
    # Após os testes, opcional: limpar tudo
    Base.metadata.drop_all(bind=engine_test)

@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sobrescrever get_db para usar o session de teste
@pytest.fixture(autouse=True)
def override_get_db(monkeypatch, db_session):
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass
    monkeypatch.setattr("backend.database.get_db", _get_test_db)

@pytest.fixture()
def client():
    return TestClient(fastapi_app)
