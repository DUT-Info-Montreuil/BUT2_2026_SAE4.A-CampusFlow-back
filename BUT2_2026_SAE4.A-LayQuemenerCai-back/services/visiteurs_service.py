from pymongo import DESCENDING
from database import db
from dtos.CreerVisiteursDTO import VisiteurCreerDTO, BacDTO, AdresseDTO, OptionsDTO
from dtos.GetVisiteursDTO import VisiteurShortDictDTO, VisiteurLongDictDTO


def get_next_id() -> int:
    dernier = db.visiteurs.find_one({}, {"_id": 1}, sort=[("_id", DESCENDING)])
    return (dernier['_id'] + 1) if dernier is not None else 0


def get_all():
    visiteurs = list(db.visiteurs.find())
    result = []
    for visiteur in visiteurs:
        visiteur_short = VisiteurShortDictDTO(
            id=visiteur['_id'],
            nom=visiteur['nom'],
            prenom=visiteur['prenom'],
            bac=visiteur['bac'],
            ville=visiteur['adresse']['ville']
        )
        result.append(visiteur_short.model_dump(exclude_none=True))
    return result


def get_visiteur_by_id(visiteur_id: int):
    visiteur = db.visiteurs.find_one({"_id": visiteur_id})
    if visiteur is None:
        return None
    visiteur_long = VisiteurLongDictDTO(
        id=visiteur['_id'],
        nom=visiteur['nom'],
        prenom=visiteur['prenom'],
        bac=visiteur['bac'],
        adresse=visiteur['adresse'],
        options=visiteur.get('options'),
        email=visiteur.get('email'),
        telephone=visiteur.get('telephone'),
        formation_actuelle=visiteur.get('formation_actuelle')
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
    if "formation_intitule" in data and "formation_niveau_etudes" in data:
        formation_actuelle = FormationActuelleDTO(
            intitule=data["formation_intitule"],
            niveau_etudes=data["formation_niveau_etudes"]
        )

    visiteur = VisiteurCreerDTO(
        nom=data["nom"],
        prenom=data["prenom"],
        date_naissance=data["date_naissance"],
        bac=bac,
        adresse=adresse
    )

    if "email" in data:
        visiteur.email = data["email"]
    if "telephone" in data:
        visiteur.telephone = data["telephone"]
    if options:
        visiteur.options = options
    if formation_actuelle:
        visiteur.formation_actuelle = formation_actuelle

    document = visiteur.model_dump(exclude_none=True)
    document['_id'] = get_next_id()
    db.visiteurs.insert_one(document)


def delete_all():
    result = db.visiteurs.delete_many({})
    return result.deleted_count
