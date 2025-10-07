from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- Configuration de la base de données ---
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://mwalimu_db_user:mWvIur0BPmkXJ2bZskADXaKemHOG2lQF@dpg-d3fae0j3fgac73b26t80-a/mwalimu_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('merci'))
    return render_template('questionnaire.html')

@app.route('/tableau')
def tableau():
    reponses = Reponse.query.all()
    return render_template('tableau_reponses.html', reponses=reponses)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée la table si elle n'existe pas
    app.run(debug=True)
