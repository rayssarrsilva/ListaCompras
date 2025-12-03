import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from models import Base
from main import app
from database import get_db

# -----------------------------
# BANCO EXCLUSIVO DE TESTE
# -----------------------------
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:123@localhost:5432/listacompras_test"
)

engine_test = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    print("✅ BANCO DE TESTE EM USO:", TEST_DATABASE_URL)
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(autouse=True)
def clean_tables():
    with engine_test.connect() as connection:
        trans = connection.begin()

        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())

        trans.commit()


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def override_get_db(db_session):
    def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db


@pytest.fixture()
def client():
    return TestClient(app)
