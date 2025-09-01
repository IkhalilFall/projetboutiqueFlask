import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "routes.login"
login_manager.login_message_category = "warning"

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["SECRET_KEY"] = "dev-secret-change-me"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
    db.init_app(app)
    login_manager.init_app(app)
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    return app

def seed_initial_data():
    from .models import User, Product, Client
    from werkzeug.security import generate_password_hash
    if not User.query.filter_by(username="admin").first():
        from . import db
        db.session.add(User(username="admin", email="admin@example.com", role="admin",
                            password_hash=generate_password_hash("admin123")))
    if not User.query.filter_by(username="vendeur").first():
        from . import db
        db.session.add(User(username="vendeur", email="vendeur@example.com", role="vendeur",
                            password_hash=generate_password_hash("vendeur123")))
    if Product.query.count() == 0:
        from . import db
        db.session.add_all([
            Product(name="T-shirt Neon", description="T-shirt noir avec motif néon", price=15.0, stock=50, image_filename="placeholder_product.png"),
            Product(name="Casquette Glow", description="Casquette logo ShopApp", price=12.0, stock=30, image_filename="placeholder_product.png"),
            Product(name="Sac Tote", description="Sac en toile robuste", price=8.5, stock=40, image_filename="placeholder_product.png"),
        ])
    if Client.query.count() == 0:
        from . import db
        db.session.add_all([
            Client(name="Alice", email="alice@mail.com", phone="01010101", address="Centre-ville"),
            Client(name="Bob", email="bob@mail.com", phone="02020202", address="Quartier Nord"),
        ])
    from . import db
    db.session.commit()
