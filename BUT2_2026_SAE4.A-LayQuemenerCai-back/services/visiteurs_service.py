import csv
from database import get_db
from mappers.visiteurs_mapper import to_short_dto, to_long_dto, to_visiteur_creer_dto


def get_all(filtres=None):
    db = get_db()
    cursor = db.execute("SELECT * FROM visiteurs")
    visiteurs = cursor.fetchall()
    result = []
    if filtres is None:
        for visiteur in visiteurs:
            result.append(to_long_dto(visiteur))
    else:
        for visiteur in visiteurs:
            condition_vraie = True
            for cle, valeur in filtres.items():
                if visiteur[cle] != valeur:
                    condition_vraie = False
                    break
            if condition_vraie:
                result.append(to_long_dto(visiteur))
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


def modif_visiteur(id_visiteur: int, data: dict):
    bac = BacDTO(
        intitule=data["bac_intitule"],
        annee=int(data["bac_annee"]),
        matiere1=data.get("bac_matiere1"),
        matiere2=data.get("bac_matiere2")
    )

    adresse = AdresseDTO(
        ville=data["adresse_ville"],
        codePostal=int(data["adresse_codePostal"])
    )

    options = None
    if "handicap" in data or "reorientation" in data or "immersion" in data:
        options = OptionsDTO(
            handicap=data.get("handicap"),
            reorientation=data.get("reorientation"),
            immersion=data.get("immersion")
        )

    formation_actuelle = None
    if "formation_actuelle_intitule" in data and "formation_actuelle_niveau" in data:
        formation_actuelle = FormationActuelleDTO(
            intitule=data["formation_actuelle_intitule"],
            niveau_etudes=data["formation_actuelle_niveau"]
        )

    lycee = LyceeDTO(
        nom_lycee=data["nom_lycee"],
        codePostal=int(data["code_postal_lycee"])
    )

    visiteur = VisiteurCreerDTO(
        nom=data["nom"],
        prenom=data["prenom"],
        date_naissance=data["date_naissance"],
        bac=bac,
        lycee=lycee,
        adresse=adresse,
        email=data.get("email"),
        telephone=data.get("telephone"),
        options=options,
        formation_actuelle=formation_actuelle
    )

    if visiteur.formation_actuelle:
        formation_intitule = visiteur.formation_actuelle.intitule
        formation_niveau = visiteur.formation_actuelle.niveau
    else:
        formation_intitule = None
        formation_niveau = None

    if visiteur.options:
        handicap = int(visiteur.options.handicap)
        reorientation = int(visiteur.options.reorientation)
        immersion = int(visiteur.options.immersion)
    else:
        handicap = 0
        reorientation = 0
        immersion = 0

    db = get_db()
    db.execute("""
        UPDATE visiteurs
        SET nom= ?,
            prenom= ?,
            email= ?,
            telephone= ?,
            date_de_naissance= ?,
            ville= ?,
            code_postal= ?,
            nom_lycee= ?,
            code_postal_lycee= ?,
            bac_intitule= ?,
            bac_annee= ?,
            bac_matiere1= ?,
            bac_matiere2= ?,
            formation_actuelle_intitule= ?,
            formation_actuelle_niveau= ?,
            handicap= ?,
            reorientation= ?,
            immersion= ?,
        WHERE id=?;
    """, (visiteur.nom, visiteur.prenom, visiteur.email, visiteur.telephone, str(visiteur.date_naissance),
          visiteur.adresse.ville, visiteur.adresse.codePostal, visiteur.lycee.nom_lycee, visiteur.lycee.codePostal,
          visiteur.bac.intitule, visiteur.bac.annee, visiteur.bac.matiere1, visiteur.bac.matiere2, formation_intitule,
          formation_niveau, handicap, reorientation, immersion, id_visiteur,))
    db.commit()


def delete_visiteur_by_id(id_visiteur: int):
    db = get_db()
    name = None
    name = db.execute("SELECT nom FROM visiteurs WHERE id= ?", (id_visiteur,))
    db.commit()
    nameF = name.fetchone()
    cursor = db.execute("DELETE FROM visiteurs WHERE id=?", (id_visiteur,))
    db.commit()
    return nameF


def delete_all():
    db = get_db()
    cursor = db.execute("DELETE FROM visiteurs")
    cursor2 = db.execute("DELETE FROM sqlite_sequence where name=?", ('visiteurs',))  # Reset l'id à 0
    db.commit()
    return cursor.rowcount


def appelle_visiteurs(filtre=None):
    db = get_db()
    if filtre:
        cursor = db.execute(
            "SELECT * FROM visiteurs WHERE (nom = :nom OR :nom IS NULL) AND (prenom = :prenom OR :prenom IS NULL) "
            "AND (email = :email OR :email IS NULL) AND (ville = :ville OR :ville IS NULL) AND (bac_intitule = :bac_intitule OR :bac_intitule IS NULL) "
            "AND (nom_lycee = :nom_lycee OR :nom_lycee IS NULL) AND (reorientation = :reorientation OR :reorientation IS NULL) "
            "AND (immersion = :immersion OR :immersion IS NULL) AND (handicap = :handicap OR :handicap IS NULL) "
            "AND (formation_actuelle_intitule = :formation_actuelle_intitule OR :formation_actuelle_intitule IS NULL)"
            "order by nom",
            filtre)

    else:
        cursor = db.execute("SELECT * FROM visiteurs")
    visiteurs = cursor.fetchall()
    return visiteurs


def fichier_csv(filtre=None):
    db = get_db()
    cursor = db.execute("PRAGMA table_info(visiteurs)")
    attribut = [a["name"] for a in cursor.fetchall()]  # recupérer les attribut de la table visiteurs
    with open('temporaire/visiteurs.csv', 'w', newline='') as csvfile:
        fieldnames = attribut  # permet de mettre les attribut en haut du fichier csv
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        visiteurs = appelle_visiteurs(filtre)
        for visiteur in visiteurs:
            writer.writerow(dict(visiteur))
    csvfile.close()
