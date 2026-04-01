from dtos.CreerConfigDTO import EvenementDTO, FormationDTO, AdresseDTO


def mapper_adresse_to_front(evenement) -> dict:
    return {
        "ville": evenement["ville"],
        "codePostal": evenement["code_postal"]
    }


def to_evenement_creer_DTO(data: dict) -> EvenementDTO:
    return EvenementDTO(
        intitule=data['intitule'],
        date=data['date'],
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


def to_short_evenement_dto(evenement) -> dict:
    return EvenementDTO(
        id=evenement["id"],
        intitule=evenement["intitule"],
        date=evenement["date"],
        adresse=mapper_adresse_to_front(evenement)
    ).model_dump(exclude_none=True)


def to_short_formation_dto(formation) -> dict:
    return FormationDTO(
        id=formation["id"],
        intitule=formation["intitule"],
        domaine=formation["domaine"],
    ).model_dump(exclude_none=True)
