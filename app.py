from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from models import db, Item, Cart
from flask_migrate import Migrate

# configuração do Flask, SQLAlchemy e rotas web
def create_app():
    app = Flask(__name__, template_folder='templates')

    # ⚠️ Ajuste a senha do seu PostgreSQL aqui (sem acentos ou caracteres especiais)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123@localhost:5432/shopping_cart_db"
    app.config['SECRET_KEY'] = "um_segredo_seguro"  # necessário para usar session

    db.init_app(app)
    Migrate(app, db)

    # rotas
    @app.route("/")
    def index():
        carts = Cart.query.all()
        selected_cart = None
        if "selected_cart_id" in session:
            selected_cart = Cart.query.get(session["selected_cart_id"])
        return render_template("index.html", carts=carts, selected_cart=selected_cart)

    @app.route("/create_cart", methods=["POST"])
    def create_cart():
        cart_name = request.form["cart_name"]
        new_cart = Cart(name=cart_name)
        db.session.add(new_cart)
        db.session.commit()
        return redirect(url_for("index"))

    @app.route("/delete/<int:cart_id>", methods=["POST"])
    def delete_cart(cart_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            return "Carrinho não encontrado", 404
        db.session.delete(cart)
        db.session.commit()
        return redirect(url_for("index"))

    @app.route("/api/itens/<int:item_id>", methods=["DELETE"])
    def delete_item(item_id):
        item = Item.query.get(item_id)
        if not item:
            return {"error": "Item não encontrado"}, 404
        db.session.delete(item)
        db.session.commit()
        return {"success": True}

    @app.route("/select_cart", methods=["POST"])
    def select_cart():
        cart_id = request.form["cart_id"]
        session["selected_cart_id"] = cart_id
        return redirect(url_for("index"))

    @app.route("/add_to_cart/<int:cart_id>", methods=["POST"])
    def add_to_cart(cart_id):
        name = request.form["name"]
        item = Item(name=name, cart_id=cart_id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("index"))

    @app.route("/api/carrinhos/<int:cart_id>/itens")
    def get_cart_items(cart_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            return jsonify({"error": "Carrinho não encontrado"}), 404
        items = Item.query.filter_by(cart_id=cart_id).all()
        return jsonify([{"id": item.id, "name": item.name} for item in items])

    @app.route("/add_bulk/<int:cart_id>", methods=["POST"])
    def add_bulk(cart_id):
        items_raw = request.form["items"]
        item_names = [name.strip() for name in items_raw.split(",") if name.strip()]
        for name in item_names:
            item = Item(name=name, cart_id=cart_id)
            db.session.add(item)
        db.session.commit()
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
