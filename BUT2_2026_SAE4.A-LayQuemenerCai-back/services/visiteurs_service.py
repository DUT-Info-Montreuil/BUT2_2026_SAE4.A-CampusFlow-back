import csv
from database import get_db
from dtos.CreerVisiteursDTO import *
from mappers.visiteurs_mapper import *
from repository.visiteurs_repository import *


def get_all(filtres=None, formation_visee=None, limit=20, page=1):
    debut = (page - 1) * limit
    visiteurs = get_allRepository(formation_visee)
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

    result = result[debut: debut + limit]
    return result


def get_visiteur_by_id(visiteur_id: int):
    visiteur = get_visiteurRepository(visiteur_id)
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
    formation_souhaitee_id = data.get("formationSouhaite")
    evenement_id = data.get("evenementSouhaite")
    add_visiteurRepository(visiteur, formation_intitule, formation_niveau, formation_souhaitee_id, evenement_id)


def modif_visiteur(id_visiteur: int, data: dict):
    bac = BacDTO(
        intitule=data["bac_intitule"],
        annee=int(data["bac_annee"]),
        matiere1=data.get("matiere1"),
        matiere2=data.get("matiere2")
    )

    adresse = AdresseDTO(
        ville=data["adresse_ville"],
        codePostal=int(data["adresse_codePostal"])
    )

    options = None
    if "handicap" in data or "immersion" in data:
        options = OptionsDTO(
            handicap=bool(data["handicap"]),
            immersion=bool(data["immersion"])
        )

    formation_actuelle = None

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
        email=data["email"],
        telephone=data["telephone"],
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
        handicap = bool(data.get("handicap", False))
        immersion = bool(data.get("immersion", False))
    else:
        handicap = 0
        immersion = 0

    update_visiteurRepository(id_visiteur, visiteur, formation_intitule, formation_niveau, handicap, immersion)


def delete_visiteur_by_id(id_visiteur: int):
    nameF = delete_visiteurRepository(id_visiteur)
    return nameF


def delete_all():
    cursor = delete_allRepository()
    return cursor.rowcount


def appelle_visiteurs(filtre=None):
    cursor = appelle_visiteurs_filtreRepository(filtre)
    visiteurs = cursor
    return visiteurs


def fichier_csv(filtre=None):
    db = get_db()
    cursor = db.execute("PRAGMA table_info(visiteurs)")
    attribut = [a["name"] for a in cursor.fetchall() if
                a["name"] != "id"]  # recupérer les attribut de la table visiteurs
    with open('temporaire/visiteurs.csv', 'w', newline='') as csvfile:
        fieldnames = attribut  # permet de mettre les attribut en haut du fichier csv
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        visiteurs = appelle_visiteurs(filtre)
        for visiteur in visiteurs:
            v = dict(visiteur)
            v.pop("id")
            writer.writerow(v)
    csvfile.close()

def appelle_email():
    cursor = appelle_visiteurs_emailRepository()
    visiteurs = cursor
    return visiteurs

def fichier_csv_email():
    with open('temporaire/email.csv', 'w', newline='') as csvfile:
        fieldnames = ["email"]  # permet de mettre les attribut en haut du fichier csv
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        emails = appelle_email()
        for email in emails:
            writer.writerow(dict(email))
    csvfile.close()


def statistique_visiteurs():
    return {'bac': stat_bac(), 'reorientation': stat_reorientation(), 'immersion': stat_immersion(),
            'handicap': stat_handicap()}


def stat_bac():
    bac = stat_bacRepository()
    return dict(bac)


def stat_reorientation():
    reorientation = stat_reorientationRepository()
    return dict(reorientation)


def stat_immersion():
    immersion = stat_immersionRepository()
    return dict(immersion)


def stat_handicap():
    handicap = stat_handicapRepository()
    return dict(handicap)
