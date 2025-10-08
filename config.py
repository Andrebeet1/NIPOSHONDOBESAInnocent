import os

class Config:
    # URL de connexion à la base de données PostgreSQL
    # Utilise DATABASE_URL depuis les variables d'environnement si défini
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://mwalimu_db_user:mWvIur0BPmkXJ2bZskADXaKemHOG2lQF@dpg-d3fae0j3fgac73b26t80-a/mwalimu_db"
    )

    # Désactive les notifications inutiles de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clé secrète pour la session Flask (changer en production)
    SECRET_KEY = os.environ.get("SECRET_KEY", "ma_cle_secrete_pour_developpement")

    # Mode debug (désactiver en production)
    DEBUG = bool(os.environ.get("DEBUG", True))
