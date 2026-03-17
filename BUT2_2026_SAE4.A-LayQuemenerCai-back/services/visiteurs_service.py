from datetime import datetime

from pymongo import MongoClient

db_uri = 'mongodb://127.0.0.1:27017/'
database = MongoClient(db_uri)
db = database.table

id_max = db.visiteurs.find_one({'$expr': {"$max": "_id"}}, {"_id": 1})
if id_max is None:
    id_max = 0
    

def get_all():
    visiteurs = list(db.visiteurs.find())
    return visiteurs


def get_visiteur_by_id(visiteur_id):
    visiteur = list(db.visiteurs.find({"_id": visiteur_id}))
    return visiteur


def add_visiteur():
    db.visiteurs.insert_one()


def delete_all():
    result = db.visiteurs.delete_many({})
    return result.deleted_count
