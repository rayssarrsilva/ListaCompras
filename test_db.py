# Crie um arquivo test_db.py na raiz
from sqlalchemy import create_engine
engine = create_engine("postgresql://postgres:123@localhost:5432/listacompras")
print("✅ Conexão bem-sucedida!")
print(engine.connect())