import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from . import db
from .models import User, Product, Client, Sale

bp = Blueprint("routes", __name__)

# --- Décorateur pour rôle ---
def role_required(role_name):
    def decorator(fn):
        from functools import wraps
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("routes.register"))
            if current_user.role != role_name:
                flash("Accès refusé.", "danger")
                return redirect(url_for("routes.home"))
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# --- Page d'accueil ---
@bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("routes.dashboard" if current_user.role=="admin" else "routes.sell"))
    return redirect(url_for("routes.register"))

# --- Inscription ---
@bp.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("routes.home"))

    if request.method == "POST":
        username = request.form.get("username","").strip()
        email = request.form.get("email","").strip()
        password = request.form.get("password","")
        confirm_password = request.form.get("confirm_password","")
        role = request.form.get("role","vendeur")  # vendeur par défaut

        if not username or not email or not password:
            flash("Veuillez remplir tous les champs.", "warning")
            return redirect(url_for("routes.register"))
        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", "danger")
            return redirect(url_for("routes.register"))

        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash("Nom d'utilisateur ou email déjà utilisé.", "warning")
            return redirect(url_for("routes.register"))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash(f"Compte créé avec succès. Bienvenue {role} !", "success")
        return redirect(url_for("routes.dashboard" if new_user.role=="admin" else "routes.sell"))

    return render_template("register.html", title="Inscription")

# --- Connexion ---
@bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f"Bienvenue {user.username} !", "success")
            return redirect(url_for("routes.dashboard" if user.role=="admin" else "routes.sell"))
        flash("Identifiants invalides.", "warning")
        return redirect(url_for("routes.login"))
    return render_template("login.html", title="Connexion")

# --- Déconnexion ---
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Déconnecté.", "info")
    return redirect(url_for("routes.register"))

# --- Dashboard admin ---
@bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    products_count = Product.query.count()
    clients_count = Client.query.count()
    sales_count = Sale.query.count()
    revenue = db.session.query(db.func.sum(Sale.total)).scalar() or 0.0
    return render_template("dashboard.html", title="Tableau de bord",
                           products_count=products_count, clients_count=clients_count,
                           sales_count=sales_count, revenue=revenue)

# --- Gestion produits ---
@bp.route("/products")
@login_required
@role_required("admin")
def products():
    q = request.args.get("q","").strip()
    items = Product.query
    if q:
        items = items.filter(Product.name.ilike(f"%{q}%"))
    items = items.order_by(Product.id.desc()).all()
    return render_template("products.html", title="Produits", items=items, q=q)

@bp.route("/products/create", methods=["GET","POST"])
@login_required
@role_required("admin")
def create_product():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        description = request.form.get("description","").strip()
        price = float(request.form.get("price","0") or 0)
        stock = int(request.form.get("stock","0") or 0)
        image_filename = None
        file = request.files.get("image")
        if file and file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            image_filename = filename
        db.session.add(Product(name=name, description=description, price=price, stock=stock, image_filename=image_filename))
        db.session.commit()
        flash("Produit ajouté.", "success")
        return redirect(url_for("routes.products"))
    return render_template("product_form.html", title="Ajouter un produit", item=None)

@bp.route("/products/<int:pid>/edit", methods=["GET","POST"])
@login_required
@role_required("admin")
def edit_product(pid):
    p = Product.query.get_or_404(pid)
    if request.method == "POST":
        p.name = request.form.get("name","").strip()
        p.description = request.form.get("description","").strip()
        p.price = float(request.form.get("price","0") or 0)
        p.stock = int(request.form.get("stock","0") or 0)
        file = request.files.get("image")
        if file and file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            p.image_filename = filename
        db.session.commit()
        flash("Produit modifié.", "success")
        return redirect(url_for("routes.products"))
    return render_template("product_form.html", title="Modifier le produit", item=p)

@bp.route("/products/<int:pid>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete_product(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash("Produit supprimé.", "info")
    return redirect(url_for("routes.products"))

# --- Gestion clients ---
@bp.route("/clients")
@login_required
@role_required("admin")
def clients():
    items = Client.query.order_by(Client.id.desc()).all()
    return render_template("clients.html", title="Clients", items=items)

@bp.route("/clients/create", methods=["GET","POST"])
@login_required
@role_required("admin")
def create_client():
    if request.method == "POST":
        c = Client(
            name=request.form.get("name","").strip(),
            email=request.form.get("email","").strip(),
            phone=request.form.get("phone","").strip(),
            address=request.form.get("address","").strip(),
        )
        db.session.add(c); db.session.commit()
        flash("Client ajouté.", "success")
        return redirect(url_for("routes.clients"))
    return render_template("client_form.html", title="Ajouter un client", item=None)

@bp.route("/clients/<int:cid>/edit", methods=["GET","POST"])
@login_required
@role_required("admin")
def edit_client(cid):
    c = Client.query.get_or_404(cid)
    if request.method == "POST":
        c.name = request.form.get("name","").strip()
        c.email = request.form.get("email","").strip()
        c.phone = request.form.get("phone","").strip()
        c.address = request.form.get("address","").strip()
        db.session.commit()
        flash("Client modifié.", "success")
        return redirect(url_for("routes.clients"))
    return render_template("client_form.html", title="Modifier le client", item=c)

@bp.route("/clients/<int:cid>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete_client(cid):
    c = Client.query.get_or_404(cid)
    db.session.delete(c); db.session.commit()
    flash("Client supprimé.", "info")
    return redirect(url_for("routes.clients"))

# --- Ventes ---
@bp.route("/sell", methods=["GET","POST"])
@login_required
def sell():
    products = Product.query.order_by(Product.name.asc()).all()
    clients = Client.query.order_by(Client.name.asc()).all()

    if request.method == "POST":
        product_id = request.form.get("product_id")
        quantity = request.form.get("quantity")
        client_id = request.form.get("client_id")

        if not product_id or not quantity:
            flash("Veuillez remplir tous les champs.", "warning")
            return redirect(url_for("routes.sell"))

        product_id = int(product_id)
        quantity = int(quantity)

        if client_id == "new":
            new_name = request.form.get("new_client_name", "").strip()
            if not new_name:
                flash("Veuillez entrer le nom du nouveau client.", "warning")
                return redirect(url_for("routes.sell"))
            c = Client(
                name=new_name,
                email=request.form.get("new_client_email", "").strip(),
                phone=request.form.get("new_client_phone", "").strip(),
                address=request.form.get("new_client_address", "").strip(),
            )
            db.session.add(c)
            db.session.flush()
            client_id = c.id
        else:
            if not client_id:
                flash("Veuillez choisir un client.", "warning")
                return redirect(url_for("routes.sell"))
            client_id = int(client_id)

        product = Product.query.get_or_404(product_id)
        if quantity <= 0:
            flash("La quantité doit être positive.", "warning")
            return redirect(url_for("routes.sell"))
        if product.stock < quantity:
            flash("Stock insuffisant.", "danger")
            return redirect(url_for("routes.sell"))

        total = round(product.price * quantity, 2)
        sale = Sale(
            client_id=client_id,
            product_id=product.id,
            quantity=quantity,
            total=total,
            user_id=current_user.id,
        )
        product.stock -= quantity
        db.session.add(sale)
        db.session.commit()

        flash("Vente enregistrée ✅", "success")
        return redirect(url_for("routes.my_sales"))

    return render_template("sell.html", title="Nouvelle vente", products=products, clients=clients)

@bp.route("/sales")
@login_required
def my_sales():
    if current_user.role == "admin":
        sales = Sale.query.order_by(Sale.created_at.desc()).all()
        title = "Toutes les ventes"
    else:
        sales = Sale.query.filter_by(user_id=current_user.id).order_by(Sale.created_at.desc()).all()
        title = "Mes ventes"
    return render_template("sales.html", title=title, sales=sales)
