import os
import io
import base64
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class Reponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200))
    gender = db.Column(db.String(20))
    marital_status = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    education_level = db.Column(db.String(50))
    household_size = db.Column(db.String(50))
    child_gender = db.Column(db.String(20))
    mother_profession = db.Column(db.String(100))
    heard_about_waterborne_diseases = db.Column(db.String(10))
    info_channel = db.Column(db.String(200))
    waterborne_disease_meaning = db.Column(db.Text)
    unsafe_water_leads_to_diseases = db.Column(db.String(10))
    known_waterborne_diseases = db.Column(db.String(300))
    know_water_treatment = db.Column(db.String(10))
    water_treatment_methods = db.Column(db.Text)
    know_handwashing_moments = db.Column(db.String(10))
    moments_lavage = db.Column(db.String(300))
    awareness_on_prevention = db.Column(db.String(10))
    awareness_channel = db.Column(db.String(300))
    source_amenee = db.Column(db.String(10))
    source_non_amenee = db.Column(db.String(10))
    lac = db.Column(db.String(10))
    riviere = db.Column(db.String(10))
    regideso = db.Column(db.String(10))
    borne_fontaine = db.Column(db.String(10))
    eau_pluie = db.Column(db.String(10))
    autres = db.Column(db.String(10))
    autres_preciser = db.Column(db.String(200))
    water_treatment_at_source = db.Column(db.String(10))
    water_treatment_method = db.Column(db.String(200))
    treat_water_before_consumption = db.Column(db.String(10))
    treatment_methods = db.Column(db.String(300))
    water_storage = db.Column(db.String(200))
    community_work = db.Column(db.String(10))
    community_work_frequency = db.Column(db.String(100))
    reason_for_not_participating = db.Column(db.String(200))
    local_water_committee = db.Column(db.String(10))
    remarks = db.Column(db.Text)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        try:
            reponse = Reponse(
                address=request.form.get('address'),
                gender=request.form.get('gender'),
                marital_status=request.form.get('marital_status'),
                religion=request.form.get('religion'),
                education_level=request.form.get('education_level'),
                household_size=request.form.get('household_size'),
                child_gender=request.form.get('child_gender'),
                mother_profession=request.form.get('mother_profession'),
                heard_about_waterborne_diseases=request.form.get('heard_about_waterborne_diseases'),
                info_channel=request.form.get('info_channel'),
                waterborne_disease_meaning=request.form.get('waterborne_disease_meaning'),
                unsafe_water_leads_to_diseases=request.form.get('unsafe_water_leads_to_diseases'),
                known_waterborne_diseases="; ".join(request.form.getlist('known_waterborne_diseases')),
                know_water_treatment=request.form.get('know_water_treatment'),
                water_treatment_methods=request.form.get('water_treatment_methods'),
                know_handwashing_moments=request.form.get('know_handwashing_moments'),
                moments_lavage="; ".join(request.form.getlist('moments_lavage')),
                awareness_on_prevention=request.form.get('awareness_on_prevention'),
                awareness_channel="; ".join(request.form.getlist('awareness_channel')),
                source_amenee=request.form.get('source_amenee'),
                source_non_amenee=request.form.get('source_non_amenee'),
                lac=request.form.get('lac'),
                riviere=request.form.get('riviere'),
                regideso=request.form.get('regideso'),
                borne_fontaine=request.form.get('borne_fontaine'),
                eau_pluie=request.form.get('eau_pluie'),
                autres=request.form.get('autres'),
                autres_preciser=request.form.get('autres_preciser'),
                water_treatment_at_source=request.form.get('water_treatment_at_source'),
                water_treatment_method=request.form.get('water_treatment_method'),
                treat_water_before_consumption=request.form.get('treat_water_before_consumption'),
                treatment_methods="; ".join(request.form.getlist('treatment_methods')),
                water_storage=request.form.get('water_storage'),
                community_work=request.form.get('community_work'),
                community_work_frequency=request.form.get('community_work_frequency'),
                reason_for_not_participating=request.form.get('reason_for_not_participating'),
                local_water_committee=request.form.get('local_water_committee'),
                remarks=request.form.get('remarks')
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
    return render_template('tableau_reponses.html', reponses=reponses)


@app.route('/delete/<int:reponse_id>', methods=['POST'])
def delete_reponse(reponse_id):
    reponse = Reponse.query.get_or_404(reponse_id)
    try:
        db.session.delete(reponse)
        db.session.commit()
        flash("Réponse supprimée avec succès.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression : {e}", "danger")
    return redirect(url_for('tableau'))


@app.route('/analyse')
def analyse():
    reponses = Reponse.query.all()
    if not reponses:
        flash("Aucune donnée disponible pour l'analyse.", "warning")
        return redirect(url_for('index'))

    data = pd.DataFrame([r.__dict__ for r in reponses]).drop('_sa_instance_state', axis=1)

    plt.figure(figsize=(5, 4))
    sns.countplot(x='gender', data=data, palette='Set2')
    plt.title("Répartition par sexe des répondants")
    plt.xlabel("Sexe")
    plt.ylabel("Nombre de répondants")

    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('analyse.html', plot_sexe=plot_url)


@app.route('/export_excel')
def export_excel():
    reponses = Reponse.query.all()

    if not reponses:
        flash("Aucune donnée disponible pour l'export.", "warning")
        return redirect(url_for('tableau'))

    data = pd.DataFrame([r.__dict__ for r in reponses]).drop('_sa_instance_state', axis=1)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        data.to_excel(writer, index=False, sheet_name="Réponses")
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="reponses_questionnaire.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)
