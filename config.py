import os

class Config:
    # URL de connexion à la base de données PostgreSQL
    SQLALCHEMY_DATABASE_URI = "postgresql://mwalimu_db_user:mWvIur0BPmkXJ2bZskADXaKemHOG2lQF@dpg-d3fae0j3fgac73b26t80-a/mwalimu_db"
    
    # Désactive les notifications inutiles de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clé secrète pour la session Flask (à changer pour la production)
    SECRET_KEY = os.environ.get("SECRET_KEY", "ma_cle_secrete_pour_developpement")

    # Options supplémentaires (facultatives)
    DEBUG = True
