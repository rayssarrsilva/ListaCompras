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
    if request.method == 'GET':
        session.pop('_flashes', None)
        return render_template('login.html')
    
    # DEBUG: Log da tentativa de login
    username = request.form['username']
    password = request.form['password']
    print(f"🔍 Tentando login: {username}")
    
    try:
        response = requests.post(f"{FASTAPI_BASE_URL}/api/login",
                               json={"username": username, "password": password},
                               timeout=10)
        print(f"🔍 Resposta API - Status: {response.status_code}")
        print(f"🔍 Resposta API - Body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            session["access_token"] = data["access_token"]
            session["username"] = username
            print(f"✅ Login bem-sucedido para: {username}")
            
            user = User(1)
            from flask_login import login_user
            login_user(user)
            return redirect(url_for('index'))
        else:
            print(f"❌ Login falhou - Status: {response.status_code}")
            flash('Usuário ou senha inválidos.', 'error')
            
    except Exception as e:
        print(f"🔥 Erro na requisição: {str(e)}")
        flash('Erro de conexão com o servidor.', 'error')
    
    return redirect(url_for('login'))

# Na rota de register, substitua TUDO por:
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Teste manual SIMPLES
        import requests
        try:
            resp = requests.post('http://localhost:8000/api/register',
                               json={'username': request.form['username'], 
                                     'password': request.form['password']},
                               timeout=3)
            if resp.status_code == 200:
                return redirect('/login')
            else:
                return f"Erro API: {resp.text}"
        except Exception as e:
            return f"Erro conexão: {str(e)}"
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
    return redirect(url_for("index"))

@app.route("/delete/<int:cart_id>", methods=["POST"])
@login_required
def delete_cart(cart_id):
    response = requests.delete(f"{FASTAPI_BASE_URL}/api/carrinhos/{cart_id}",
                              headers=get_auth_headers())
    return redirect(url_for("index"))

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
    return redirect(url_for("index"))

@app.route("/api/carrinhos/<int:cart_id>/itens")
@login_required
def get_cart_items(cart_id):
    response = requests.get(f"{FASTAPI_BASE_URL}/api/carrinhos/{cart_id}/itens",
                           headers=get_auth_headers())
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Carrinho não encontrado"}), 404

@app.route("/add_bulk/<int:cart_id>", methods=["POST"])
@login_required
def add_bulk(cart_id):
    items_raw = request.form["items"]
    item_names = [name.strip() for name in items_raw.split(",") if name.strip()]
    response = requests.post(f"{FASTAPI_BASE_URL}/api/carrinhos/{cart_id}/bulk",
                           json={"items": item_names},
                           headers=get_auth_headers())
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)