from app import app, db
from sqlalchemy import text  # ✅ à importer

# On exécute dans le contexte Flask
with app.app_context():
    with db.engine.connect() as conn:
        alter_query = text("""
            ALTER TABLE reponse
            ALTER COLUMN address TYPE VARCHAR(200),
            ALTER COLUMN gender TYPE VARCHAR(50),
            ALTER COLUMN marital_status TYPE VARCHAR(100),
            ALTER COLUMN religion TYPE VARCHAR(100),
            ALTER COLUMN education_level TYPE VARCHAR(100),
            ALTER COLUMN household_size TYPE VARCHAR(50),
            ALTER COLUMN child_gender TYPE VARCHAR(50),
            ALTER COLUMN mother_profession TYPE VARCHAR(150),
            ALTER COLUMN heard_about_waterborne_diseases TYPE VARCHAR(50),
            ALTER COLUMN info_channel TYPE VARCHAR(300),
            ALTER COLUMN unsafe_water_leads_to_diseases TYPE VARCHAR(50),
            ALTER COLUMN known_waterborne_diseases TYPE VARCHAR(500),
            ALTER COLUMN know_water_treatment TYPE VARCHAR(50),
            ALTER COLUMN water_treatment_methods TYPE VARCHAR(500),
            ALTER COLUMN know_handwashing_moments TYPE VARCHAR(50),
            ALTER COLUMN moments_lavage TYPE VARCHAR(500),
            ALTER COLUMN awareness_on_prevention TYPE VARCHAR(50),
            ALTER COLUMN awareness_channel TYPE VARCHAR(500),
            ALTER COLUMN source_amenee TYPE VARCHAR(50),
            ALTER COLUMN source_non_amenee TYPE VARCHAR(50),
            ALTER COLUMN lac TYPE VARCHAR(50),
            ALTER COLUMN riviere TYPE VARCHAR(50),
            ALTER COLUMN regideso TYPE VARCHAR(50),
            ALTER COLUMN borne_fontaine TYPE VARCHAR(50),
            ALTER COLUMN eau_pluie TYPE VARCHAR(50),
            ALTER COLUMN autres TYPE VARCHAR(50),
            ALTER COLUMN autres_preciser TYPE VARCHAR(300),
            ALTER COLUMN water_treatment_at_source TYPE VARCHAR(50),
            ALTER COLUMN water_treatment_method TYPE VARCHAR(300),
            ALTER COLUMN treat_water_before_consumption TYPE VARCHAR(50),
            ALTER COLUMN treatment_methods TYPE VARCHAR(500),
            ALTER COLUMN water_storage TYPE VARCHAR(300),
            ALTER COLUMN community_work TYPE VARCHAR(50),
            ALTER COLUMN community_work_frequency TYPE VARCHAR(200),
            ALTER COLUMN reason_for_not_participating TYPE VARCHAR(300),
            ALTER COLUMN local_water_committee TYPE VARCHAR(50);
        """)

        conn.execute(alter_query)  # ✅ exécution correcte
        conn.commit()

    print("✅ Les colonnes ont été agrandies avec succès !")
