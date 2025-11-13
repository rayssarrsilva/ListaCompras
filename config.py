import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:123@localhost:5432/shopping_cart_db')
SECRET_KEY = 'your-secret-key'