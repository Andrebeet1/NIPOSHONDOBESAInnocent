import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

from config import Config  # ⚡ Import de la configuration

# -------------------------------------------------------
# Initialisation de l'application Flask
# -------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)  # ⚡ Charger la config

db = SQLAlchemy(app)

# -------------------------------------------------------
# Modèle de la base de données
# -------------------------------------------------------
class Reponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adresse = db.Column(db.String(200))
    sexe = db.Column(db.String(20))
    statut_matrimonial = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    niveau_etude = db.Column(db.String(50))
    taille_menage = db.Column(db.String(50))
    sexe_enfant = db.Column(db.String(20))
    profession_mere = db.Column(db.String(100))
    entendu_maladie_hydrique = db.Column(db.String(10))
    canal_information = db.Column(db.String(200))
    definition_maladie_hydrique = db.Column(db.Text)
    eau_insalubre_maladie = db.Column(db.String(10))
    maladies_connues = db.Column(db.String(300))
    connaissance_traitement_eau = db.Column(db.String(10))
    moyens_traitement_eau = db.Column(db.Text)
    connaissance_lavage_mains = db.Column(db.String(10))
    moments_lavage_mains = db.Column(db.String(300))
    sensibilisation_prevention = db.Column(db.String(10))
    canal_sensibilisation = db.Column(db.String(300))
    source_eau = db.Column(db.String(300))
    eau_traitee = db.Column(db.String(10))
    mode_traitement = db.Column(db.String(200))
    traitement_menage = db.Column(db.String(10))
    methode_traitement_menage = db.Column(db.String(200))
    stockage_eau = db.Column(db.String(200))
    participation_travaux = db.Column(db.String(10))
    frequence_travaux = db.Column(db.String(100))
    raison_non_participation = db.Column(db.String(200))
    maladie_enfant = db.Column(db.String(10))
    type_maladie = db.Column(db.String(200))

# -------------------------------------------------------
# Routes principales
# -------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        try:
            reponse = Reponse(
                adresse=request.form.get('adresse'),
                sexe=request.form.get('sexe'),
                statut_matrimonial=request.form.get('statut_matrimonial'),
                religion=request.form.get('religion'),
                niveau_etude=request.form.get('niveau_etude'),
                taille_menage=request.form.get('taille_menage'),
                sexe_enfant=request.form.get('sexe_enfant'),
                profession_mere=request.form.get('profession_mere'),
                entendu_maladie_hydrique=request.form.get('entendu_maladie_hydrique'),
                canal_information=request.form.get('canal_information'),
                definition_maladie_hydrique=request.form.get('definition_maladie_hydrique'),
                eau_insalubre_maladie=request.form.get('eau_insalubre_maladie'),
                maladies_connues="; ".join(request.form.getlist('maladies_connues')),
                connaissance_traitement_eau=request.form.get('connaissance_traitement_eau'),
                moyens_traitement_eau=request.form.get('moyens_traitement_eau'),
                connaissance_lavage_mains=request.form.get('connaissance_lavage_mains'),
                moments_lavage_mains="; ".join(request.form.getlist('moments_lavage_mains')),
                sensibilisation_prevention=request.form.get('sensibilisation_prevention'),
                canal_sensibilisation="; ".join(request.form.getlist('canal_sensibilisation')),
                source_eau="; ".join(request.form.getlist('source_eau')),
                eau_traitee=request.form.get('eau_traitee'),
                mode_traitement=request.form.get('mode_traitement'),
                traitement_menage=request.form.get('traitement_menage'),
                methode_traitement_menage=request.form.get('methode_traitement_menage'),
                stockage_eau=request.form.get('stockage_eau'),
                participation_travaux=request.form.get('participation_travaux'),
                frequence_travaux=request.form.get('frequence_travaux'),
                raison_non_participation=request.form.get('raison_non_participation'),
                maladie_enfant=request.form.get('maladie_enfant'),
                type_maladie=request.form.get('type_maladie'),
            )
            db.session.add(reponse)
            db.session.commit()
            flash("Merci ! Vos réponses ont été enregistrées avec succès.", "success")
            return redirect(url_for('merci'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'enregistrement : {e}", "danger")

    return render_template('questionnaire.html')

@app.route('/merci')
def merci():
    return render_template('merci.html')

@app.route('/tableau')
def tableau():
    reponses = Reponse.query.all()
    return render_template('dashboard.html', reponses=reponses)

@app.route('/analyse')
def analyse():
    reponses = Reponse.query.all()
    if not reponses:
        flash("Aucune donnée disponible pour l'analyse.", "warning")
        return redirect(url_for('index'))

    data = pd.DataFrame([r.__dict__ for r in reponses]).drop('_sa_instance_state', axis=1)

    plt.figure(figsize=(5, 4))
    sns.countplot(x='sexe', data=data, palette='Set2')
    plt.title("Répartition par sexe des répondants")
    plt.xlabel("Sexe")
    plt.ylabel("Nombre de répondants")

    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('analyse.html', plot_sexe=plot_url)

# -------------------------------------------------------
# Création de la base au premier lancement
# -------------------------------------------------------
with app.app_context():
    db.create_all()

# -------------------------------------------------------
# Lancement de l'application
# -------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)
