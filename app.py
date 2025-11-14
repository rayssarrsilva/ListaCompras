from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from models import db, Item, Cart, User, UserRoles, Role
import config
from flask_migrate import Migrate

#cconfiguração do flask, sqlalchemy e rotas web
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SECURITY_PASSWORD_SALT'] = 'um_salt_seguro'
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_RECOVERABLE'] = True
    app.config['SECURITY_TRACKABLE'] = True
    app.config['SECURITY_RENDER_TEMPLATE_EXT'] = '.html'
    app.config['SECURITY_FLASH_MESSAGES'] = True
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False  # se não quiser email de confirmação
    
    app.config['SECURITY_POST_REGISTER_VIEW'] = 'security.login'
    app.config['SECURITY_POST_LOGOUT_VIEW'] = 'security.login'
    app.config['SECURITY_MSG_USER_EXISTS'] = ('Esse email já está cadastrado.', 'error')
    
    app.config['SECURITY_MSG_PASSWORD_INVALID'] = ('Senha inválida.', 'error')
    app.config['SECURITY_MSG_PASSWORD_MISMATCH'] = ('As senhas não conferem.', 'error')
    app.config['SECURITY_MSG_RETYPE_PASSWORD_MISMATCH'] = ('As senhas digitadas não são iguais.', 'error')
    app.config['SECURITY_MSG_EMAIL_NOT_PROVIDED'] = ('Você precisa informar um email.', 'error')
    app.config['SECURITY_MSG_PASSWORD_NOT_PROVIDED'] = ('Você precisa informar uma senha.', 'error')

    
    db.init_app(app)
    migrate = Migrate(app, db)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # rotas ficam dentro da função
    @app.route('/')
    @login_required
    def index():
        carts = Cart.query.all()
        selected_cart = None
        if 'selected_cart_id' in session:
            selected_cart = Cart.query.get(session['selected_cart_id'])
        return render_template('index.html', carts=carts, selected_cart=selected_cart)

    @app.route('/create_cart', methods=['POST'])
    def create_cart():
        cart_name = request.form['cart_name']
        new_cart = Cart(name=cart_name)
        db.session.add(new_cart)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/delete/<int:cart_id>', methods=['POST'])
    def delete_cart(cart_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            return "Carrinho não encontrado", 404
        db.session.delete(cart)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/api/itens/<int:item_id>', methods=['DELETE'])
    def delete_item(item_id):
        item = Item.query.get(item_id)
        if not item:
            return {"error": "Item não encontrado"}, 404
        db.session.delete(item)
        db.session.commit()
        return {"success": True}

    @app.route('/select_cart', methods=['POST'])
    def select_cart():
        cart_id = request.form['cart_id']
        session['selected_cart_id'] = cart_id
        return redirect(url_for('index'))

    @app.route('/add_to_cart/<int:cart_id>', methods=['POST'])
    def add_to_cart(cart_id):
        name = request.form['name']
        item = Item(name=name, cart_id=cart_id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/api/carrinhos/<int:cart_id>/itens')
    def get_cart_items(cart_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            return jsonify({"error": "Carrinho não encontrado"}), 404
        items = Item.query.filter_by(cart_id=cart_id).all()
        return jsonify([{"id": item.id, "name": item.name} for item in items])

    @app.route('/add_bulk/<int:cart_id>', methods=['POST'])
    def add_bulk(cart_id):
        items_raw = request.form['items']
        item_names = [name.strip() for name in items_raw.split(',') if name.strip()]
        for name in item_names:
            item = Item(name=name, cart_id=cart_id)
            db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)