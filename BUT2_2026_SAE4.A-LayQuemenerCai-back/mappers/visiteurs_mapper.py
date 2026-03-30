from dtos.CreerVisiteursDTO import (VisiteurCreerDTO, BacDTO, LyceeDTO, AdresseDTO, OptionsDTO, FormationActuelleDTO)
from dtos.GetVisiteursDTO import VisiteurShortDictDTO, VisiteurLongDictDTO

"""
    Cette fonction permet de passer de mapper la section bac issu de la bdd 
    vers la version qui va être retourné au front end
"""


def mapper_bac_to_front(visiteur) -> dict:
    return {
        "intitule": visiteur["bac_intitule"],
        "annee": visiteur["bac_annee"],
        "matiere1": visiteur["bac_matiere1"],
        "matiere2": visiteur["bac_matiere2"]
    }


"""
    Cette fonction permet de passer de mapper la section de l'adresse du visiteur 
    issu de la bdd vers la version qui va être retourné au front end
"""


def mapper_adresse_to_front(visiteur) -> dict:
    return {
        "ville": visiteur["ville"],
        "codePostal": visiteur["code_postal"]
    }


"""
    Cette fonction permet de passer de mapper la section du lycée du visiteur 
    issu de la bdd vers la version qui va être retourné au front end
"""


def mapper_lycee_to_front(visiteur) -> dict:
    return {
        "nom_lycee": visiteur["nom_lycee"],
        "codePostal": visiteur["code_postal_lycee"]
    }


"""
    Cette fonction permet de passer de mapper la section liées aux options du visiteurs 
    issu de la bdd vers la version qui va être retourné au front end
"""


def mapper_options_to_front(visiteur):
    return OptionsDTO(
        handicap=bool(visiteur["handicap"]),
        reorientation=bool(visiteur["reorientation"]),
        immersion=bool(visiteur["immersion"])
    ).model_dump()


"""
    Cette fonction permet de passer de mapper la section liée au formation actuelle 
    du visiteur (si il est en réorientation) issu de la bdd 
    vers la version qui va être retourné au front end
"""


def mapper_formation_actuelle_to_front(visiteur):
    if visiteur["formation_actuelle_intitule"] and visiteur["formation_actuelle_niveau"]:
        return FormationActuelleDTO(
            intitule=visiteur["formation_actuelle_intitule"],
            niveau_etudes=visiteur["formation_actuelle_niveau"]
        )
    return None


"""
    Cette fonction permet de passer de mapper les données du visiteur du bdd 
    vers la version qui va être retourné au front end
"""


def to_short_dto(visiteur) -> dict:
    return VisiteurShortDictDTO(
        id=visiteur["id"],
        nom=visiteur["nom"],
        prenom=visiteur["prenom"],
        bac=mapper_bac_to_front(visiteur),
        adresse=mapper_adresse_to_front(visiteur)
    ).model_dump(exclude_none=True)


"""
    Cette fonction permet de passer de mapper les données du visiteur du bdd 
    vers la version qui va être retourné au front end
"""


def to_long_dto(visiteur) -> dict:
    return VisiteurLongDictDTO(
        id=visiteur["id"],
        nom=visiteur["nom"],
        prenom=visiteur["prenom"],
        bac=mapper_bac_to_front(visiteur),
        lycee=mapper_lycee_to_front(visiteur),
        adresse=mapper_adresse_to_front(visiteur),
        options=mapper_options_to_front(visiteur),
        email=visiteur["email"],
        telephone=visiteur["telephone"],
        formation_actuelle=mapper_formation_actuelle_to_front(visiteur)
    ).model_dump(exclude_none=True)


"""
    Cette fonction permet de passer de mapper les données du visiteur issus du front end 
    vers la version qui va être inséré au bdd
"""


def to_visiteur_creer_dto(data: dict) -> VisiteurCreerDTO:
    if "formation_actuelle_intitule" in data and "formation_actuelle_niveau" in data:
        formation_actuelle_attribut = FormationActuelleDTO(
            intitule=data["formation_actuelle_intitule"],
            niveau_etudes=data["formation_actuelle_niveau"]
        )
    else:
        formation_actuelle_attribut = None

    return VisiteurCreerDTO(
        nom=data["nom"],
        prenom=data["prenom"],
        date_naissance=data["date_naissance"],
        email=data.get("email"),
        telephone=data.get("telephone"),
        bac=BacDTO(
            intitule=data["bac_intitule"],
            annee=int(data["bac_annee"]),
            matiere1=data.get("bac_matiere1"),
            matiere2=data.get("bac_matiere2")
        ),
        lycee=LyceeDTO(
            nom_lycee=data["nom_lycee"],
            codePostal=int(data["code_postal_lycee"])
        ),
        adresse=AdresseDTO(
            ville=data["adresse_ville"],
            codePostal=int(data["adresse_codePostal"])
        ),
        options=OptionsDTO(
            handicap=bool(data.get("handicap", False)),
            reorientation=bool(data.get("reorientation", False)),
            immersion=bool(data.get("immersion", False))
        ),
        formation_actuelle=formation_actuelle_attribut
    )
