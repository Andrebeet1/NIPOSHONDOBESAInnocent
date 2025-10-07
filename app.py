import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt

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

    # Convertir en DataFrame
    data = []
    for r in reponses:
        data.append({
            "sexe": r.sexe,
            "niveau_etude": r.niveau_etude,
            "taille_menage": r.taille_menage,
            "connaissance_maladie": r.connaissance_maladie,
            "participation_travaux": r.participation_travaux,
            "enfant_maladie": r.enfant_maladie
        })
    df = pd.DataFrame(data)

    # Tableaux croisés
    croisement1 = pd.crosstab(df['niveau_etude'], df['connaissance_maladie'], margins=True)
    croisement2 = pd.crosstab(df['taille_menage'], df['participation_travaux'], margins=True)
    croisement3 = pd.crosstab(df.get('eau_insalubre', pd.Series(['Oui']*len(df))), df['enfant_maladie'], margins=True)

    # Graphique empilé : niveau d'étude vs connaissance des maladies
    plt.figure(figsize=(8,5))
    croisement1.iloc[:-1,:-1].plot(kind='bar', stacked=True, color=['skyblue','salmon'])
    plt.title("Connaissance des maladies selon le niveau d'étude")
    plt.ylabel("Nombre de réponses")
    plt.xlabel("Niveau d'étude")
    plt.tight_layout()

    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    graph1_url = base64.b64encode(buf1.getvalue()).decode()
    buf1.close()
    graph1_url = 'data:image/png;base64,' + graph1_url

    return render_template(
        'analyse_comparaison.html',
        croisement1=croisement1.to_html(classes='table table-bordered table-sm table-striped'),
        croisement2=croisement2.to_html(classes='table table-bordered table-sm table-striped'),
        croisement3=croisement3.to_html(classes='table table-bordered table-sm table-striped'),
        graph1_url=graph1_url
    )

@app.route('/problemes_sanitaires')
def problemes_sanitaires():
    return render_template('problemes_sanitaires.html')

@app.route('/planification_locale')
def planification_locale():
    return render_template('planification_locale.html')

@app.route('/decisions_publiques')
def decisions_publiques():
    return render_template('decisions_publiques.html')

@app.route('/merci')
def merci():
    return render_template('merci.html')

# --- Démarrage de l'application ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)