from datetime import datetime

from pymongo import MongoClient

db_uri = 'mongodb://127.0.0.1:27017/'
database = MongoClient(db_uri)
db = database.table

def get_all():
    visiteurs = list(db.visiteurs.find())
    return visiteurs


def get_visiteur_by_id(visiteur_id):
    visiteur = list(db.visiteurs.find({"_id": visiteur_id}))
    return visiteur
