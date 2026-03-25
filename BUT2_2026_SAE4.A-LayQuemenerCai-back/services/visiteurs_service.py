from database import get_db
from dtos.CreerVisiteursDTO import VisiteurCreerDTO, BacDTO, LyceeDTO, AdresseDTO, OptionsDTO, FormationActuelleDTO
from dtos.GetVisiteursDTO import VisiteurShortDictDTO, VisiteurLongDictDTO


def get_all():
    db = get_db()
    cursor = db.execute("SELECT * FROM visiteurs")
    visiteurs = cursor.fetchall()
    result = []
    for visiteur in visiteurs:
        bac = {
            "intitule": visiteur["bac_intitule"],
            "annee": visiteur["bac_annee"],
            "matiere1": visiteur["bac_matiere1"],
            "matiere2": visiteur["bac_matiere2"]
        }
        adresse = {
            "ville": visiteur["ville"],
            "codePostal": visiteur["code_postal"]
        }
        visiteur_short = VisiteurShortDictDTO(
            id=visiteur["id"],
            nom=visiteur["nom"],
            prenom=visiteur["prenom"],
            bac=bac,
            adresse=adresse
        )
        result.append(visiteur_short.model_dump(exclude_none=True))
    return result


def get_visiteur_by_id(visiteur_id: int):
    db = get_db()
    cursor = db.execute("SELECT * FROM visiteurs WHERE id=?", (visiteur_id,))
    visiteur = cursor.fetchone()
    if not visiteur:
        return None

    bac = {
        "intitule": visiteur["bac_intitule"],
        "annee": visiteur["bac_annee"],
        "matiere1": visiteur["bac_matiere1"],
        "matiere2": visiteur["bac_matiere2"]
    }
    adresse = {
        "ville": visiteur["ville"],
        "codePostal": visiteur["code_postal"]
    }
    lycee = {
        "nom_lycee": visiteur["nom_lycee"],
        "codePostal": visiteur["code_postal_lycee"]
    }
    options = None
    if visiteur["handicap"] or visiteur["reorientation"] or visiteur["immersion"]:
        options = OptionsDTO(
            handicap=bool(visiteur["handicap"]),
            reorientation=bool(visiteur["reorientation"]),
            immersion=bool(visiteur["immersion"])
        )

    formation_actuelle = None
    if visiteur["formation_actuelle_intitule"] and visiteur["formation_actuelle_niveau"]:
        formation_actuelle = FormationActuelleDTO(
            intitule=visiteur["formation_actuelle_intitule"],
            niveau_etudes=visiteur["formation_actuelle_niveau"]
        )

    visiteur_long = VisiteurLongDictDTO(
        id=visiteur["id"],
        nom=visiteur["nom"],
        prenom=visiteur["prenom"],
        bac=bac,
        lycee=lycee,
        adresse=adresse,
        options=options,
        email=visiteur["email"],
        telephone=visiteur["telephone"],
        formation_actuelle=formation_actuelle
    )
    return visiteur_long.model_dump(exclude_none=True)


def add_visiteur(data: dict):
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
        handicap,
        reorientation,
        immersion
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
        SET nom= visiteur.nom,
            prenom= visiteur.prenom,
            email= visiteur.email,
            telephone= visiteur.telephone,
            date_de_naissance= str(visiteur.date_naissance),
            ville= visiteur.adresse.ville,
            code_postal= visiteur.adresse.codePostal,
            nom_lycee= visiteur.lycee.nom_lycee,
            code_postal_lycee= visiteur.lycee.codePostal,
            bac_intitule= visiteur.bac.intitule,
            bac_annee= visiteur.bac.annee,
            bac_matiere1= visiteur.bac.matiere1,
            bac_matiere2= visiteur.bac.matiere2,
            formation_actuelle_intitule= formation_intitule,
            formation_actuelle_niveau= formation_niveau,
            handicap= handicap,
            reorientation= reorientation,
            immersion= immersion
        WHERE id=id_visiteur;
    """,)
    db.commit()


def delete_visiteur_by_id(id_visiteur: int):
    db = get_db()
    name = None
    name = db.execute("SELECT nom FROM visiteurs WHERE id= ?", (id_visiteur,))
    nameF = name.fetchone()
    cursor = db.execute("DELETE FROM visiteurs WHERE id=?", (id_visiteur,))
    db.commit()
    return name


def delete_all():
    db = get_db()
    cursor = db.execute("DELETE FROM visiteurs")
    db.commit()
    return cursor.rowcount
