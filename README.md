# projetboutiqueFlask
🛍️ Application de Gestion de Boutique avec Flask
📖 Description

Cette application web interne permet à une petite boutique de gérer ses produits, clients et ventes de manière simple et intuitive.
Développée avec Flask (Python), elle propose une interface moderne et sécurisée pour le personnel de la boutique.

🎯 Objectifs pédagogiques

Mettre en pratique le développement web avec Flask/Python

Manipuler une base de données (SQLite, MySQL ou PostgreSQL)

Gérer les opérations CRUD (Create, Read, Update, Delete)

Implémenter une authentification avec rôles (Admin & Vendeur)

Déploiement local ou sur un serveur gratuit (optionnel)

✨ Fonctionnalités
1. Gestion des produits

Ajouter un produit (nom, description, prix, stock, image optionnelle)

Modifier/Supprimer un produit

Lister les produits avec recherche et filtrage

2. Gestion des clients

Ajouter un client (nom, email, téléphone, adresse)

Modifier/Supprimer un client

Lister tous les clients

3. Gestion des ventes

Enregistrer une nouvelle vente (client, produits, quantités)

Calcul automatique du montant total

Historique des ventes avec date, client et montant

4. Authentification & Rôles

Connexion/Déconnexion

Administrateur : accès complet

Vendeur : accès limité

🏗️ Technologies utilisées

Backend : Flask (Python 3)

Base de données : SQLite (par défaut) / MySQL / PostgreSQL

Frontend : HTML, CSS (Bootstrap), JavaScript (optionnel)

⚙️ Installation et configuration
1. Cloner le projet
git clone https://github.com/ton-utilisateur/gestion-boutique-flask.git
cd gestion-boutique-flask

2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Installer les dépendances
pip install -r requirements.txt

4. Configurer la base de données

Par défaut, l’application utilise SQLite.
Vous pouvez modifier la configuration dans config.py pour utiliser MySQL ou PostgreSQL.

5. Initialiser la base de données
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

6. Lancer l’application
flask run


L’application sera disponible sur : http://localhost:5000

📂 Structure du projet
gestion-boutique-flask/
│
├── app/
│   ├── static/            # Fichiers CSS, JS, images
│   ├── templates/         # Templates HTML (Jinja2)
│   ├── models.py          # Modèles de base de données
│   ├── routes.py          # Routes Flask
│   ├── forms.py           # Formulaires (WTForms)
│   └── __init__.py        # Initialisation Flask
│
├── migrations/            # Fichiers de migration DB
├── config.py              # Configuration de l'app
├── requirements.txt       # Dépendances Python
├── run.py                 # Point d'entrée principal
└── README.md              # Documentation du projet

👤 Rôles et accès
Rôle	Accès complet	Gestion Produits	Gestion Clients	Historique des ventes
Admin	✅	✅	✅	✅
Vendeur	❌	✅	✅	✅
🚀 Déploiement (Optionnel)

Déploiement possible sur Render, Railway ou PythonAnywhere

Support pour Heroku (avec Procfile)

📝 Auteur

Ibrahima Khalil FALL – Développeur Python/Flask
📧 Email : khalilfall52@gmail.com

📜 Licence

Ce projet est sous licence MIT – vous êtes libre de le modifier et de le distribuer.
