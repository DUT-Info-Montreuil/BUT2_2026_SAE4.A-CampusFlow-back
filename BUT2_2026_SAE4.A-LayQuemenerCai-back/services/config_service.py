import os
from database import get_db
from dotenv import set_key
from dotenv import load_dotenv
from mappers.config_mapper import *
from dtos.CreerConfigDTO import *
from repository.config_repository import *


def get_evenement_all():
    evenement = get_evenement_allRepository()
    result = []
    for event in evenement:
        result.append(to_short_evenement_dto(event))
    return result


def add_evenement(data: dict):
    evenement = to_evenement_creer_DTO(data)
    add_evenementRepository(evenement)


def delete_evenement_all():
    cursor = delete_evenement_allRepository()
    return cursor.rowcount


def delete_evenement_by_id(id_evenement: int):
    nameF = delete_evenement_by_idRepository(id_evenement)
    return nameF


def modif_evenement(id_evenement: int, data: dict):
    adresse = AdresseDTO(
        ville=data["adresse_ville"],
        codePostal=int(data["adresse_codePostal"])
    )
    evenement = EvenementDTO(
        intitule=data['evenement_intitule'],
        lieu=adresse,
        date=str(data['date'])
    )
    modif_evenementRepository(id_evenement, evenement)


def get_formation_all():
    formation = get_formation_allRepository()
    result = []
    for event in formation:
        result.append(to_short_formation_dto(event))
    return result


def add_formation(data: dict):
    formation = to_formation_creer_DTO(data)
    add_formationRepository(formation)


def delete_formation_all():
    cursor = delete_formation_allRepository()
    return cursor.rowcount


def delete_formation_by_id(id_formation: int):
    nameF = delete_formation_by_idRepository(id_formation)
    return nameF

def modif_password(data):
    if (data["newPassword"] == data["confPassword"] and password_ok(data["oldPassword"])):
        load_dotenv(override=True)
        set_key(".env","PASSWORD",data["newPassword"])
    
def modif_formation(id_formation: int, data: dict):
    adresse = AdresseDTO(
        ville=data["adresse_ville"],
        codePostal=int(data["adresse_codePostal"])
    )
    formation = FormationDTO(
        intitule=data['formation_intitule'],
        lieu=adresse
    )
    modif_formationRepository(id_formation, formation)


def password_ok(password: str):
    load_dotenv()
    if password == os.getenv("PASSWORD"):
        return True
    return False

