# frontend/auth.py (versão corrigida — OPCIONAL)
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests

auth = Blueprint('auth', __name__)
FASTAPI_BASE_URL = "http://localhost:8000"

@auth.route('/login', methods=['GET', 'POST'])
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
            # Simular login com Flask-Login (opcional)
            from frontend.app import User, login_user
            user = User(1)  # ID fictício
            login_user(user)
            return redirect(url_for('index'))
        flash('Usuário ou senha inválidos.', 'error')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f"{FASTAPI_BASE_URL}/api/register",
                               json={"username": username, "password": password})
        if response.status_code == 200:
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Nome de usuário já existe.', 'error')
    return render_template('register.html')

@auth.route('/logout')
def logout():
    session.clear()
    from flask_login import logout_user
    logout_user()
    return redirect(url_for('auth.login'))