import os
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from models import db, Item, Cart, User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates')

    # Usa as variáveis do .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    with app.app_context():
        db.create_all()  # Cria as tabelas conforme models.py

    @app.route("/")
    @login_required
    def index():
        carts = Cart.query.filter_by(user_id=current_user.id).all()
        selected_cart = None
        if "selected_cart_id" in session:
            selected_cart = Cart.query.filter_by(id=session["selected_cart_id"], user_id=current_user.id).first()
        return render_template("index.html", carts=carts, selected_cart=selected_cart)

    @app.route("/create_cart", methods=["POST"])
    @login_required
    def create_cart():
        cart_name = request.form["cart_name"]
        new_cart = Cart(name=cart_name, user_id=current_user.id)
        db.session.add(new_cart)
        db.session.commit()
        return redirect(url_for("index"))

    @app.route("/delete/<int:cart_id>", methods=["POST"])
    @login_required
    def delete_cart(cart_id):
        cart = Cart.query.filter_by(id=cart_id, user_id=current_user.id).first_or_404()
        db.session.delete(cart)
        db.session.commit()
        return redirect(url_for("index"))

    @app.route("/api/itens/<int:item_id>", methods=["DELETE"])
    @login_required
    def delete_item(item_id):
        item = Item.query.join(Cart).filter(Item.id == item_id, Cart.user_id == current_user.id).first()
        if not item:
            return {"error": "Item não encontrado"}, 404
        db.session.delete(item)
        db.session.commit()
        return {"success": True}

    @app.route("/select_cart", methods=["POST"])
    @login_required
    def select_cart():
        cart_id = request.form["cart_id"]
        cart = Cart.query.filter_by(id=cart_id, user_id=current_user.id).first()
        if cart:
            session["selected_cart_id"] = cart.id
        return redirect(url_for("index"))

    @app.route("/add_to_cart/<int:cart_id>", methods=["POST"])
    @login_required
    def add_to_cart(cart_id):
        cart = Cart.query.filter_by(id=cart_id, user_id=current_user.id).first_or_404()
        name = request.form["name"]
        item = Item(name=name, cart_id=cart.id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("index"))

    @app.route("/api/carrinhos/<int:cart_id>/itens")
    @login_required
    def get_cart_items(cart_id):
        cart = Cart.query.filter_by(id=cart_id, user_id=current_user.id).first()
        if not cart:
            return jsonify({"error": "Carrinho não encontrado"}), 404
        items = Item.query.filter_by(cart_id=cart.id).all()
        return jsonify([{"id": item.id, "name": item.name} for item in items])

    @app.route("/add_bulk/<int:cart_id>", methods=["POST"])
    @login_required
    def add_bulk(cart_id):
        cart = Cart.query.filter_by(id=cart_id, user_id=current_user.id).first_or_404()
        items_raw = request.form["items"]
        item_names = [name.strip() for name in items_raw.split(",") if name.strip()]
        for name in item_names:
            item = Item(name=name, cart_id=cart.id)
            db.session.add(item)
        db.session.commit()
        return redirect(url_for("index"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5000)