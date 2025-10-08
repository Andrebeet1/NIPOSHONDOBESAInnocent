import os
from app import db, app

with app.app_context():
    db.drop_all()  # Supprime toutes les tables
    db.create_all()  # Crée toutes les tables
    print("Base de données réinitialisée avec succès.")
