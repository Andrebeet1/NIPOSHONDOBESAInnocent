from app import db, app

with app.app_context():
    print("❌ Suppression de toutes les tables...")
    db.drop_all()
    print("✅ Tables supprimées.")

    print("🔄 Création des tables...")
    db.create_all()
    print("✅ Tables créées avec succès.")
