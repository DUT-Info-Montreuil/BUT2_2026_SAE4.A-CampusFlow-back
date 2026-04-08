import csv
from database import get_db
from mappers.visiteurs_mapper import *
from repository.visiteurs_repository import *


def get_all(filtres=None, limit=20, page=1):
    debut = (page - 1) * limit
    visiteurs = get_allRepository()
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
    add_visiteurRepository(visiteur, formation_intitule, formation_niveau)


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

    update_visiteurRepository(id_visiteur, visiteur, formation_intitule, formation_niveau, handicap, reorientation, immersion)


def delete_visiteur_by_id(id_visiteur: int):
    nameF = delete_visiteurRepository(id_visiteur)
    return nameF


def delete_all():
    cursor = delete_allRepository()
    return cursor.rowcount


def appelle_visiteurs(filtre=None):
    if filtre:
        cursor = appelle_visiteurs_filtreRepository(filtre)
    else:
        cursor = get_allRepository()
    visiteurs = cursor
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
