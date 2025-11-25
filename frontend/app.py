import os
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash
from flask_login import LoginManager, login_required, UserMixin
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

FASTAPI_BASE_URL = "http://localhost:8000"

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def get_auth_headers():
    token = session.get("access_token")
    return {"Authorization": f"Bearer {token}"} if token else {}

# --- Autenticação ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f"{FASTAPI_BASE_URL}/api/login",
                               json={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            session["access_token"] = data["access_token"]
            session["username"] = username
            user = User(1)  # Simula ID (não usado no backend)
            from flask_login import login_user
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f"{FASTAPI_BASE_URL}/api/register",
                               json={"username": username, "password": password})
        if response.status_code == 200:
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Nome de usuário já existe.', 'error')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    from flask_login import logout_user
    logout_user()
    return redirect(url_for('login'))

# --- Interface Principal ---
@app.route("/")
@login_required
def index():
    response = requests.get(f"{FASTAPI_BASE_URL}/api/carrinhos",
                           headers=get_auth_headers())
    carts = response.json() if response.status_code == 200 else []
    return render_template("index.html", carts=carts, selected_cart=None)

@app.route("/create_cart", methods=["POST"])
@login_required
def create_cart():
    cart_name = request.form["cart_name"]
    response = requests.post(f"{FASTAPI_BASE_URL}/api/carrinhos",
                           json={"name": cart_name},
                           headers=get_auth_headers())
    return redirect(url_for("index")) if response.status_code == 200 else redirect(url_for("index"))

@app.route("/delete/<int:cart_id>", methods=["POST"])
@login_required
def delete_cart(cart_id):
    response = requests.delete(f"{FASTAPI_BASE_URL}/api/carrinhos/{cart_id}",
                              headers=get_auth_headers())
    return redirect(url_for("index")) if response.status_code == 200 else redirect(url_for("index"))

@app.route("/select_cart", methods=["POST"])
@login_required
def select_cart():
    cart_id = request.form["cart_id"]
    session["selected_cart_id"] = cart_id
    return redirect(url_for("index"))

@app.route("/add_to_cart/<int:cart_id>", methods=["POST"])
@login_required
def add_to_cart(cart_id):
    name = request.form["name"]
    response = requests.post(f"{FASTAPI_BASE_URL}/api/carrinhos/{cart_id}/itens",
                           json={"name": name},
                           headers=get_auth_headers())
    return redirect(url_for("index")) if response.status_code == 200 else redirect(url_for("index"))

@app.route("/add_bulk/<int:cart_id>", methods=["POST"])
@login_required
def add_bulk(cart_id):
    items_raw = request.form["items"]
    item_names = [name.strip() for name in items_raw.split(",") if name.strip()]
    response = requests.post(f"{FASTAPI_BASE_URL}/api/carrinhos/{cart_id}/bulk",
                           json={"items": item_names},
                           headers=get_auth_headers())
    return redirect(url_for("index")) if response.status_code == 200 else redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)