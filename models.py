from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.Integer, default=0, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id', ondelete='CASCADE'), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # nome do carrinho
    items = db.relationship('Item', backref='cart', lazy=True, cascade="all, delete")
