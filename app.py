import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = "supersecretkey"  # nécessaire pour les flash messages

# --- Configuration de la base de données ---
db_url = os.getenv(
    "DATABASE_URL",
    "postgresql://mwalimu_db_user:mWvIur0BPmkXJ2bZskADXaKemHOG2lQF@dpg-d3fae0j3fgac73b26t80-a/mwalimu_db"
)

# Correction du préfixe pour compatibilité psycopg3
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- Modèle de données ---
class Reponse(db.Model):
    __tablename__ = "reponses"

    id = db.Column(db.Integer, primary_key=True)
    adresse = db.Column(db.String(255))
    sexe = db.Column(db.String(20))
    statut_matrimonial = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    niveau_etude = db.Column(db.String(50))
    taille_menage = db.Column(db.String(50))
    profession = db.Column(db.String(50))
    connaissance_maladie = db.Column(db.String(10))
    canal_information = db.Column(db.String(200))
    signification_maladie = db.Column(db.Text)
    eau_insalubre = db.Column(db.String(10))
    maladies_connues = db.Column(db.Text)
    connaissance_traitement = db.Column(db.String(10))
    moyens_traitement = db.Column(db.Text)
    connaissance_lavage_mains = db.Column(db.String(10))
    moments_lavage = db.Column(db.Text)
    sensibilisation_prevention = db.Column(db.String(10))
    canal_sensibilisation = db.Column(db.String(200))
    source_eau = db.Column(db.String(200))
    eau_traitee_source = db.Column(db.String(10))
    methode_traitement_source = db.Column(db.String(200))
    traitement_avant_consommation = db.Column(db.String(10))
    methode_traitement = db.Column(db.String(200))
    stockage_eau = db.Column(db.String(200))
    participation_travaux = db.Column(db.String(10))
    frequence_participation = db.Column(db.String(200))
    raison_non_participation = db.Column(db.String(200))
    enfant_maladie = db.Column(db.String(10))
    nom_maladie = db.Column(db.String(200))

    def __repr__(self):
        return f"<Réponse {self.id}>"

# --- Routes principales ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        data = Reponse(
            adresse=request.form.get('address'),
            sexe=request.form.get('gender'),
            statut_matrimonial=request.form.get('marital_status'),
            religion=request.form.get('religion'),
            niveau_etude=request.form.get('education_level'),
            taille_menage=request.form.get('household_size'),
            profession=request.form.get('mother_profession'),
            connaissance_maladie=request.form.get('heard_about_waterborne_diseases'),
            canal_information=request.form.get('info_channel'),
            signification_maladie=request.form.get('waterborne_disease_meaning'),
            eau_insalubre=request.form.get('unsafe_water_leads_to_diseases'),
            maladies_connues=request.form.get('known_waterborne_diseases'),
            connaissance_traitement=request.form.get('know_water_treatment'),
            moyens_traitement=request.form.get('water_treatment_methods'),
            connaissance_lavage_mains=request.form.get('know_handwashing_moments'),
            moments_lavage=",".join(request.form.getlist('moments_lavage')),
            sensibilisation_prevention=request.form.get('awareness_on_prevention'),
            canal_sensibilisation=request.form.get('awareness_channel'),
            source_eau=request.form.get('water_supply_source'),
            eau_traitee_source=request.form.get('water_treatment_at_source'),
            methode_traitement_source=request.form.get('water_treatment_method'),
            traitement_avant_consommation=request.form.get('treat_water_before_consumption'),
            methode_traitement=request.form.get('treatment_methods'),
            stockage_eau=request.form.get('water_storage'),
            participation_travaux=request.form.get('community_work'),
            frequence_participation=request.form.get('community_work_frequency'),
            raison_non_participation=request.form.get('reason_for_not_participating'),
            enfant_maladie=request.form.get('child_waterborne_disease_contact'),
            nom_maladie=request.form.get('disease_name')
        )
        try:
            db.session.add(data)
            db.session.commit()
            flash("Réponse enregistrée avec succès !", "success")
        except Exception:
            db.session.rollback()
            flash("Erreur lors de l’enregistrement.", "danger")
        return redirect(url_for('questionnaire'))
    return render_template('questionnaire.html')

@app.route('/tableau')
def tableau():
    try:
        reponses = Reponse.query.all()
    except Exception:
        db.create_all()
        reponses = []
    return render_template('tableau_reponses.html', reponses=reponses)

@app.route('/delete_reponse/<int:reponse_id>', methods=['POST'])
def delete_reponse(reponse_id):
    reponse = Reponse.query.get_or_404(reponse_id)
    try:
        db.session.delete(reponse)
        db.session.commit()
        flash("Réponse supprimée avec succès !", "success")
    except Exception:
        db.session.rollback()
        flash("Erreur lors de la suppression.", "danger")
    return redirect(url_for('tableau'))

# --- Analyse comparative ---
@app.route('/analyse_comparaison')
def analyse_comparaison():
    reponses = Reponse.query.all()
    if not reponses:
        flash("Aucune donnée disponible pour l'analyse.", "warning")
        return redirect(url_for('tableau'))

    # Transformation en DataFrame
    data = pd.DataFrame([{
        "sexe": r.sexe,
        "niveau_etude": r.niveau_etude,
        "participation_travaux": r.participation_travaux,
        "connaissance_traitement": r.connaissance_traitement
    } for r in reponses])

    def plot_to_base64(fig):
        img = BytesIO()
        fig.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()

    # Graphiques
    # 1. Répartition par sexe
    fig1, ax1 = plt.subplots()
    sns.countplot(x='sexe', data=data, ax=ax1)
    ax1.set_title("Répartition par sexe")
    plot_sexe = plot_to_base64(fig1)
    plt.close(fig1)

    # 2. Répartition par niveau d’étude
    fig2, ax2 = plt.subplots()
    sns.countplot(x='niveau_etude', data=data, ax=ax2)
    ax2.set_title("Répartition par niveau d’étude")
    plot_etude = plot_to_base64(fig2)
    plt.close(fig2)

    # 3. Participation aux travaux selon le sexe
    fig3, ax3 = plt.subplots()
    sns.countplot(x='participation_travaux', hue='sexe', data=data, ax=ax3)
    ax3.set_title("Participation aux travaux selon le sexe")
    plot_participation_sexe = plot_to_base64(fig3)
    plt.close(fig3)

    # 4. Connaissance du traitement selon niveau d’étude
    fig4, ax4 = plt.subplots()
    sns.countplot(x='niveau_etude', hue='connaissance_traitement', data=data, ax=ax4)
    ax4.set_title("Connaissance traitement selon niveau d’étude")
    plot_traitement_etude = plot_to_base64(fig4)
    plt.close(fig4)

    return render_template(
        'analyse_comparaison.html',
        plot_sexe=plot_sexe,
        plot_etude=plot_etude,
        plot_participation_sexe=plot_participation_sexe,
        plot_traitement_etude=plot_traitement_etude
    )

@app.route('/merci')
def merci():
    return render_template('merci.html')

# --- Démarrage ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)