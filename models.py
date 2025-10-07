from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reponse(db.Model):
    __tablename__ = "reponses"

    id = db.Column(db.Integer, primary_key=True)

    # I. Caractéristique sociodémographique
    adresse = db.Column(db.String(255), nullable=False)
    sexe = db.Column(db.String(20), nullable=False)
    statut_matrimonial = db.Column(db.String(50), nullable=False)
    religion = db.Column(db.String(50), nullable=False)
    niveau_etude = db.Column(db.String(50), nullable=False)
    taille_menage = db.Column(db.String(50), nullable=False)
    sexe_enfant = db.Column(db.String(20), nullable=False)
    profession_mere = db.Column(db.String(100), nullable=False)

    # II. Connaissance de la population
    connaissance_maladie = db.Column(db.String(10), nullable=False)
    canal_information = db.Column(db.String(100))
    signification_maladie = db.Column(db.Text)
    consommation_eau_insalubre = db.Column(db.String(10))
    maladies_connues = db.Column(db.Text)
    connaissance_traitement = db.Column(db.String(10))
    moyens_traitement = db.Column(db.Text)
    connaissance_lavage_mains = db.Column(db.String(10))
    moments_lavage = db.Column(db.Text)
    sensibilisation_prevention = db.Column(db.String(10))
    canal_sensibilisation = db.Column(db.String(100))

    # III. Niveau de recours
    source_eau = db.Column(db.String(100))
    eau_traitee_source = db.Column(db.String(10))
    methode_traitement_source = db.Column(db.String(100))
    traitement_avant_consommation = db.Column(db.String(10))
    methode_traitement = db.Column(db.String(100))
    stockage_eau = db.Column(db.String(100))
    participation_travaux = db.Column(db.String(10))
    frequence_participation = db.Column(db.String(50))
    raison_non_participation = db.Column(db.String(100))

    # IV. Prévalence
    enfant_maladie = db.Column(db.String(10))
    nom_maladie = db.Column(db.String(100))

    def __repr__(self):
        return f"<Reponse {self.id} - {self.adresse}>"
