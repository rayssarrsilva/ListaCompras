from flask import Flask, render_template, redirect, url_for, request, session
from models import db, Item, Cart
import config, os 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SECRET_KEY'] = config.SECRET_KEY
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
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
    cart = Cart.query.get(cart_id)  # busca no banco
    if not cart:
        return "Carrinho não encontrado", 404
    
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('index'))  # volta para a página inicial

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

@app.route('/add_bulk/<int:cart_id>', methods=['POST'])
def add_bulk(cart_id):
    items_raw = request.form['items']
    item_names = [name.strip() for name in items_raw.split(',') if name.strip()]
    for name in item_names:
        item = Item(name=name, cart_id=cart_id)
        db.session.add(item)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
