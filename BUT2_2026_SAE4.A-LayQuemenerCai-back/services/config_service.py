import csv
import os

from database import get_db
from dotenv import set_key
from flask.cli import load_dotenv
from mappers.config_mapper import *


def get_evenement_all():
    db = get_db
    cursor = db.execute("SELECT * FROM evenement")
    evenement = cursor.fetchall()
    result = []
    for event in evenement:
        result.append(to_short_dto(event))
    return result


def add_evenement(data: dict):
    db = get_db()
    evenement = to_evenement_creer_DTO(data)
    db.execute("""
    INSERT INTO evenement (intitule,lieu,date)
    VALUES (?,?)""",(
        evenement.intitule,
        evenement.lieu
    ))
    db.commit()


def delete_evenement_all():
    db = get_db()
    cursor = db.execute("DELETE FROM evenement")
    cursor2 = db.execute("DELETE FROM sqlite_sequence where name=?", ('evenement',)) # Reset l'id à 0
    db.commit()
    return cursor.rowcount


def delete_evenement_by_id(id_evenement: int):
    db = get_db()
    name = None
    name = db.execute("SELECT nom FROM evenement WHERE id= ?", (id_evenement,))
    db.commit()
    nameF = name.fetchone()
    cursor = db.execute("DELETE FROM evenement WHERE id=?", (id_evenement,))
    db.commit()
    return nameF


# def modif_evenement(id_evenement: int, data: dict):
#     evenement =
#     db = get_db()
#     db.execute("""
#     UPDATE evenement
#     SET intitule= ?,
#         lieu= ?,
#     WHERE id= ?;""",(
#         evenement.intitule,
#         evenement.lieu
#     ))
#     db.commit()

def get_formation_all():
    db = get_db
    cursor = db.execute("SELECT * FROM formation_iut")
    formation = cursor.fetchall()
    result = []
    for event in formation:
        result.append(to_short_dto(event))
    return result


def add_formation(data: dict):
    db = get_db()
    formation = to_formation_creer_DTO(data)
    db.execute("""
    INSERT INTO formation_iut (intitule,domaine)
    VALUES (?,?)""",(
        formation.intitule,
        formation.domaine
    ))
    db.commit()


def delete_formation_all():
    db = get_db()
    cursor = db.execute("DELETE FROM formation_iut")
    cursor2 = db.execute("DELETE FROM sqlite_sequence where name=?", ('formation',)) # Reset l'id à 0
    db.commit()
    return cursor.rowcount


def delete_formation_by_id(id_formation: int):
    db = get_db()
    name = None
    name = db.execute("SELECT nom FROM formation_iut WHERE id= ?", (id_formation,))
    db.commit()
    nameF = name.fetchone()
    cursor = db.execute("DELETE FROM formation_iut WHERE id=?", (id_formation,))
    db.commit()
    return nameF


# def modif_formation(id_formation: int, data: dict):
#     formation =
#     db = get_db()
#     db.execute("""
#     UPDATE formation
#     SET intitule= ?,
#         lieu= ?,
#     WHERE id= ?;""",(
#         formation.intitule,
#         formation.lieu
#     ))
#     db.commit()



def modif_password(data):
    load_dotenv()
    set_key(".env","PASSWORD",data)
    domaine=os.getenv("DOMAIN")
    return domaine
