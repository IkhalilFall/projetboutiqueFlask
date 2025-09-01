from app import create_app, db, seed_initial_data
import os

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        os.makedirs(os.path.join(app.root_path, "static", "uploads"), exist_ok=True)
        db.create_all()
        seed_initial_data()
    app.run(debug=True)
