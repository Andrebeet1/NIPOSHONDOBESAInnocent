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
    try:
        reponses = Reponse.query.all()
        return render_template('tableau_reponses.html', reponses=reponses)
    except Exception as e:
        flash(f"Erreur lors du chargement des données : {e}", "danger")
        return redirect(url_for('index'))


@app.route('/delete/<int:reponse_id>', methods=['POST'])
def delete_reponse(reponse_id):
    try:
        reponse = Reponse.query.get_or_404(reponse_id)
        db.session.delete(reponse)
        db.session.commit()
        flash("Réponse supprimée avec succès.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression : {e}", "danger")
    return redirect(url_for('tableau'))


@app.route('/analyse')
def analyse():
    try:
        reponses = Reponse.query.all()
        if not reponses:
            flash("Aucune donnée disponible pour l'analyse.", "warning")
            return redirect(url_for('index'))

        # Convertir en DataFrame
        data = pd.DataFrame([r.__dict__ for r in reponses]).drop('_sa_instance_state', axis=1)

        plots = {}        # Dictionnaire pour les graphiques
        tables = {}       # Dictionnaire pour les tableaux
        commentaires = {} # Dictionnaire pour les commentaires

        # -----------------------------
        # 1️⃣ Répartition par sexe
        # -----------------------------
        tab_sexe = data['gender'].value_counts().reset_index()
        tab_sexe.columns = ['Sexe', 'Nombre']
        tables['table_sexe'] = tab_sexe.to_html(index=False)

        commentaires['commentaire_sexe'] = (
            f"Sur {len(data)} répondants, "
            f"{tab_sexe.loc[tab_sexe['Sexe']=='Femme', 'Nombre'].values[0]} sont des femmes "
            f"et {tab_sexe.loc[tab_sexe['Sexe']=='Homme', 'Nombre'].values[0]} sont des hommes."
        )

        plt.figure(figsize=(5,4))
        sns.countplot(x='gender', data=data, palette='Set2')
        plt.title("Répartition par sexe")
        plt.xlabel("Sexe")
        plt.ylabel("Nombre de répondants")
        img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plots['plot_sexe'] = base64.b64encode(img.getvalue()).decode()
        plt.close()

        # -----------------------------
        # 2️⃣ Répartition par niveau d'éducation
        # -----------------------------
        tab_edu = data['education_level'].value_counts().reset_index()
        tab_edu.columns = ['Niveau d’éducation', 'Nombre']
        tables['table_education'] = tab_edu.to_html(index=False)

        commentaires['commentaire_education'] = (
            f"La majorité des mères ont un niveau d’éducation {tab_edu.iloc[0,0]} "
            f"avec {tab_edu.iloc[0,1]} répondants sur {len(data)}."
        )

        plt.figure(figsize=(6,4))
        sns.countplot(x='education_level', data=data, palette='Set3', order=tab_edu['Niveau d’éducation'])
        plt.title("Répartition par niveau d'éducation")
        plt.xlabel("Niveau d'éducation")
        plt.ylabel("Nombre de répondants")
        img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plots['plot_education'] = base64.b64encode(img.getvalue()).decode()
        plt.close()

        # -----------------------------
        # 3️⃣ Connaissance des maladies hydriques
        # -----------------------------
        tab_connaissance = data['heard_about_waterborne_diseases'].value_counts().reset_index()
        tab_connaissance.columns = ['Connaît maladies', 'Nombre']
        tables['table_connaissance'] = tab_connaissance.to_html(index=False)

        commentaires['commentaire_connaissance'] = (
            f"{tab_connaissance.loc[tab_connaissance['Connaît maladies']=='Oui','Nombre'].values[0]} répondants "
            f"connaissent les maladies hydriques sur {len(data)}."
        )

        plt.figure(figsize=(4,4))
        sns.countplot(x='heard_about_waterborne_diseases', data=data, palette='Set2')
        plt.title("Connaissance des maladies hydriques")
        plt.xlabel("Oui / Non")
        plt.ylabel("Nombre")
        img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plots['plot_connaissance'] = base64.b64encode(img.getvalue()).decode()
        plt.close()

        # -----------------------------
        # 4️⃣ Traitement de l'eau avant consommation
        # -----------------------------
        tab_traitement = data['treat_water_before_consumption'].value_counts().reset_index()
        tab_traitement.columns = ['Traite eau avant consommation', 'Nombre']
        tables['table_traitement'] = tab_traitement.to_html(index=False)

        commentaires['commentaire_traitement'] = (
            f"{tab_traitement.loc[tab_traitement['Traite eau avant consommation']=='Oui','Nombre'].values[0]} répondants "
            f"traitent l'eau avant consommation sur {len(data)}."
        )

        plt.figure(figsize=(4,4))
        sns.countplot(x='treat_water_before_consumption', data=data, palette='Set3')
        plt.title("Traitement de l’eau avant consommation")
        plt.xlabel("Oui / Non")
        plt.ylabel("Nombre")
        img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plots['plot_traitement'] = base64.b64encode(img.getvalue()).decode()
        plt.close()

        # -----------------------------
        # 5️⃣ Sources d'eau utilisées (multi-réponse)
        # -----------------------------
        sources = ['source_amenee', 'source_non_amenee', 'lac', 'riviere', 'regideso', 'borne_fontaine', 'eau_pluie', 'autres']
        sources_count = {s: (data[s] == 'Oui').sum() for s in sources}
        tab_sources = pd.DataFrame(list(sources_count.items()), columns=['Source', 'Nombre'])
        tables['table_sources'] = tab_sources.to_html(index=False)

        commentaires['commentaire_sources'] = "La source d'eau la plus utilisée est {} avec {} répondants.".format(
            tab_sources.iloc[0,0], tab_sources.iloc[0,1]
        )

        plt.figure(figsize=(6,4))
        sns.barplot(x='Source', y='Nombre', data=tab_sources, palette='Set1')
        plt.title("Sources d'eau utilisées")
        plt.ylabel("Nombre de répondants")
        plt.xticks(rotation=45)
        img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plots['plot_sources'] = base64.b64encode(img.getvalue()).decode()
        plt.close()

        # -----------------------------
        # 6️⃣ Corrélation entre pratiques et connaissances
        # -----------------------------
        bin_cols = ['heard_about_waterborne_diseases', 'know_water_treatment', 'know_handwashing_moments', 'treat_water_before_consumption', 'community_work', 'local_water_committee']
        bin_data = data[bin_cols].replace({'Oui': 1, 'Non': 0})
        corr = bin_data.corr()
        tables['table_corr'] = corr.to_html()

        commentaires['commentaire_corr'] = "La heatmap montre les associations entre connaissances et pratiques : valeurs proches de 1 indiquent une forte corrélation positive."

        plt.figure(figsize=(6,5))
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title("Corrélation entre pratiques et connaissances")
        img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plots['plot_corr'] = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return render_template('analyse.html', plots=plots, tables=tables, commentaires=commentaires)

    except Exception as e:
        flash(f"Erreur lors de l'analyse : {e}", "danger")
        return redirect(url_for('index'))


@app.route('/export_excel')
def export_excel():
    try:
        reponses = Reponse.query.all()
        if not reponses:
            flash("Aucune donnée disponible pour l'export.", "warning")
            return redirect(url_for('tableau'))

        # Création d'un DataFrame avec colonnes distinctes
        data = pd.DataFrame([
            {
                "Adresse": r.address,
                "Sexe": r.gender,
                "Statut matrimonial": r.marital_status,
                "Religion": r.religion,
                "Niveau d’étude": r.education_level,
                "Taille de ménage": r.household_size,
                "Sexe de l’enfant": r.child_gender,
                "Profession de la mère": r.mother_profession,
                "Entendu parler des maladies hydriques": r.heard_about_waterborne_diseases,
                "Canal d’information": r.info_channel,
                "Signification maladie hydrique": r.waterborne_disease_meaning,
                "Eau insalubre mène aux maladies": r.unsafe_water_leads_to_diseases,
                "Connaissances des maladies": r.known_waterborne_diseases,
                "Connaissance traitement eau": r.know_water_treatment,
                "Méthodes de traitement eau": r.water_treatment_methods,
                "Connaissance moments lavage mains": r.know_handwashing_moments,
                "Moments lavage mains": r.moments_lavage,
                "Sensibilisation prévention": r.awareness_on_prevention,
                "Canal sensibilisation": r.awareness_channel,
                "Source aménagée": r.source_amenee,
                "Source non aménagée": r.source_non_amenee,
                "Lac": r.lac,
                "Rivière": r.riviere,
                "Regideso": r.regideso,
                "Borne fontaine": r.borne_fontaine,
                "Eau de pluie": r.eau_pluie,
                "Autres": r.autres,
                "Préciser autres": r.autres_preciser,
                "Eau traitée au point de puisage": r.water_treatment_at_source,
                "Méthode traitement au point de puisage": r.water_treatment_method,
                "Traite l’eau avant consommation": r.treat_water_before_consumption,
                "Méthodes de traitement": r.treatment_methods,
                "Stockage de l’eau": r.water_storage,
                "Travaux communautaires": r.community_work,
                "Fréquence travaux communautaires": r.community_work_frequency,
                "Raison de non-participation": r.reason_for_not_participating,
                "Comité local de l’eau": r.local_water_committee,
                "Remarques": r.remarks
            } for r in reponses
        ])

        # Export Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            data.to_excel(writer, index=False, sheet_name="Questionnaire")
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="questionnaire_ibanda.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        flash(f"Erreur lors de l'export Excel : {e}", "danger")
        return redirect(url_for('tableau'))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)
