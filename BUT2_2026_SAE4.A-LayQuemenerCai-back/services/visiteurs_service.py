import csv
from database import get_db
from mappers.visiteurs_mapper import to_short_dto, to_long_dto, to_visiteur_creer_dto


def get_all():
    db = get_db()
    cursor = db.execute("SELECT * FROM visiteurs")
    visiteurs = cursor.fetchall()
    result = []
    for visiteur in visiteurs:
        result.append(to_short_dto(visiteur))
    return result


def get_visiteur_by_id(visiteur_id: int):
    db = get_db()
    cursor = db.execute("SELECT * FROM visiteurs WHERE id=?", (visiteur_id,))
    visiteur = cursor.fetchone()
    if not visiteur:
        return None
    else:
        return to_long_dto(visiteur)


def add_visiteur(data: dict):
    visiteur = to_visiteur_creer_dto(data)

    if visiteur.formation_actuelle:
        formation_intitule = visiteur.formation_actuelle.intitule
        formation_niveau = visiteur.formation_actuelle.niveau
    else:
        formation_intitule = None
        formation_niveau = None

    db = get_db()
    db.execute("""
        INSERT INTO visiteurs (
            nom, prenom, email, telephone, date_de_naissance, ville, code_postal,
            nom_lycee, code_postal_lycee, bac_intitule, bac_annee, bac_matiere1, bac_matiere2,
            formation_actuelle_intitule, formation_actuelle_niveau, handicap, reorientation, immersion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        visiteur.nom,
        visiteur.prenom,
        visiteur.email,
        visiteur.telephone,
        str(visiteur.date_naissance),
        visiteur.adresse.ville,
        visiteur.adresse.codePostal,
        visiteur.lycee.nom_lycee,
        visiteur.lycee.codePostal,
        visiteur.bac.intitule,
        visiteur.bac.annee,
        visiteur.bac.matiere1,
        visiteur.bac.matiere2,
        formation_intitule,
        formation_niveau,
        visiteur.options.handicap,
        visiteur.options.reorientation,
        visiteur.options.immersion
    ))
    db.commit()


def delete_all():
    db = get_db()
    cursor = db.execute("DELETE FROM visiteurs")
    cursor2 = db.execute("DELETE FROM sqlite_sequence where name=?", ('visiteurs',)) # Reset l'id à 0
    db.commit()
    return cursor.rowcount


def appelle_visiteurs():
    db = get_db()
    cursor = db.execute("SELECT * FROM visiteurs")
    visiteurs = cursor.fetchall()
    return visiteurs


def fichier_csv():
    db = get_db()
    cursor = db.execute("PRAGMA table_info(visiteurs)")
    attribut = [a["name"] for a in cursor.fetchall()]  # recupérer les attribut de la table visiteurs
    with open('temporaire/visiteurs.csv', 'w', newline='') as csvfile:
        fieldnames = attribut  # permet de mettre les attribut en haut du fichier csv
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        visiteurs = appelle_visiteurs()
        for visiteur in visiteurs:
            writer.writerow(dict(visiteur))
    csvfile.close()
