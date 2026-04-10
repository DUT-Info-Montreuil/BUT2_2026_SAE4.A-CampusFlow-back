import sqlite3
import os

def init_db():
    init = sqlite3.connect(os.getenv("DATABASE"))
    init.executescript("""
        CREATE TABLE IF NOT EXISTS evenements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intitule TEXT NOT NULL,
            lieu TEXT DEFAULT NULL,
            code_postal INTEGER DEFAULT NULL,
            date DATE DEFAULT NULL
        );

        CREATE TABLE IF NOT EXISTS formations_iut (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intitule TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS visiteurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT DEFAULT NULL,
            telephone TEXT DEFAULT NULL,
            date_de_naissance DATE NOT NULL,
            ville TEXT NOT NULL,
            code_postal INTEGER NOT NULL,
            nom_lycee TEXT DEFAULT NULL,
            code_postal_lycee INTEGER DEFAULT NULL,
            bac_intitule TEXT NOT NULL,
            bac_annee INTEGER NOT NULL,
            bac_matiere1 TEXT DEFAULT NULL,
            bac_matiere2 TEXT DEFAULT NULL,
            formation_actuelle_intitule TEXT DEFAULT NULL,
            formation_actuelle_niveau TEXT DEFAULT NULL,
            handicap BOOLEAN DEFAULT 0,
            reorientation BOOLEAN DEFAULT 0,
            immersion BOOLEAN DEFAULT 0,
            CONSTRAINT email_ou_tel CHECK (email IS NOT NULL OR telephone IS NOT NULL)
        );

        CREATE TABLE IF NOT EXISTS choix_formations_visees (
            visiteur_id INTEGER REFERENCES visiteurs(id) ON DELETE CASCADE,
            formation_id INTEGER REFERENCES formations_iut(id) ON DELETE CASCADE,
            PRIMARY KEY (visiteur_id, formation_id)
        );

        CREATE TABLE IF NOT EXISTS evenements_participes (
            visiteur_id INTEGER REFERENCES visiteurs(id) ON DELETE CASCADE,
            evenement_id INTEGER REFERENCES evenements(id) ON DELETE CASCADE,
            PRIMARY KEY (visiteur_id, evenement_id)
        );
    """)
    init.commit()
    init.close()
