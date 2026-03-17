from pymongo import MongoClient, DESCENDING

db_uri = 'mongodb://127.0.0.1:27017/'
database = MongoClient(db_uri)
db = database.table

db.visiteurs.drop()
dernier = db.visiteurs.find_one({}, {"_id": 1}, sort=[("_id", DESCENDING)], limit = 1)
_idMax = (dernier['_id'] + 1) if dernier is not None else 0


def get_all():
    visiteurs = list(db.visiteurs.find())
    return visiteurs


def get_visiteur_by_id(visiteur_id):
    visiteur = list(db.visiteurs.find({"_id": visiteur_id}))
    return visiteur


def add_visiteur(donnée: dict):
    global _idMax
    donnée['_id'] = _idMax
    db.visiteurs.insert_one(donnée)
    _idMax += 1

def delete_visiteurs():
    db.visiteurs.drop()


