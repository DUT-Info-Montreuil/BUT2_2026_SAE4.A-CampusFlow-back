from dtos.CreerConfigDTO import EvenementDTO, FormationDTO, AdresseDTO


def mapper_adresse_to_front(evenement) -> dict:
    return {
        "ville": evenement["ville"],
        "codePostal": evenement["code_postal"]
    }


def to_evenement_creer_DTO(data: dict) -> EvenementDTO:
    return EvenementDTO(
        intitule=data['intitule'],
        data=data['date'],
        lieu=AdresseDTO(
            ville=data["adresse_ville"],
            codePostal=int(data["adresse_codePostal"])
        )
    )


def to_formation_creer_DTO(data: dict) -> FormationDTO:
    return FormationDTO(
        intitule=data['intitule'],
        domaine=data['domaine']
    )


def to_short_dto(visiteur) -> dict:
    return VisiteurShortDictDTO(
        id=visiteur["id"],
        nom=visiteur["nom"],
        prenom=visiteur["prenom"],
        bac=mapper_bac_to_front(visiteur),
        adresse=mapper_adresse_to_front(visiteur)
    ).model_dump(exclude_none=True)
