from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="vendeur", nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_filename = db.Column(db.String(255), nullable=True)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(200))

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship("Client", backref="sales")
    product = db.relationship("Product", backref="sales")
    seller = db.relationship("User", backref="sales")
