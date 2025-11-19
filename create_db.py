# create_db.py
from app import create_app
from models import db, User, Cart, Item  # ← explícito para garantir carregamento

app = create_app()

with app.app_context():
    # Verifica se as tabelas existem
    inspector = db.inspect(db.engine)
    existing_tables = inspector.get_table_names()
    
    print("🛠️ Tabelas existentes:", existing_tables)
    
    if not existing_tables:
        print("🚀 Criando tabelas...")
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
    else:
        print("✅ Tabelas já existem. Nada a fazer.")