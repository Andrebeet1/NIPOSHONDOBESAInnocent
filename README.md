# Questionnaire d’enquête - Zone de Santé d’Ibanda

## 📌 Description du projet
Ce projet est une application web développée avec **Flask**, **Bootstrap** et **AJAX**, ayant pour objectif de collecter des données fiables auprès des responsables de ménages dans la Zone de Santé d’Ibanda.  
Ces données permettront :
- D’identifier les problèmes sanitaires.
- D’orienter la planification locale.
- De soutenir les décisions de santé publique.

---

## 🎯 Objectifs
- Faciliter la collecte d’informations à travers un questionnaire interactif.
- Stocker les réponses dans une base de données PostgreSQL.
- Offrir une interface claire pour consulter les réponses collectées.
- Générer des données exploitables pour la santé publique.

---

## 📂 Structure du projet

questionnaire_ibanda/
│
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── runtime.txt
├── README.md
│
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── questionnaire.html
│ ├── tableau_reponses.html
│ ├── problemes_sanitaires.html
│ ├── planification_locale.html
│ ├── decisions_publiques.html
│ ├── merci.html
│
├── static/
│ ├── css/
│ │ └── style.css