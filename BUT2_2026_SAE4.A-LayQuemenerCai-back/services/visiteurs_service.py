from pymongo import MongoClient, DESCENDING
import csv

db_uri = 'mongodb://127.0.0.1:27017/'
database = MongoClient(db_uri)
db = database.table

db.visiteurs.drop()
dernier = db.visiteurs.find_one({}, {"_id": 1}, sort=[("_id", DESCENDING)], limit=1)
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


def delete_all():
    result = db.visiteurs.delete_many({})
    return result.deleted_count

def trier_visiteurs(donnee: dict):
    #les 3 ligne servent a renvoyer uniquement les collones a afficher donner dans le dictionnaire

    visiteurs = list(db.visiteurs.find(donnee))
    print(visiteurs)
    return visiteurs

def fichier_csv(donnee: dict):
    with open('visiteurs.csv', 'w', newline='') as csvfile:
        fieldnames = ["_id","nom","prenom"] #permet de mettre les attribut en haut du fichier csv
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        visiteurs = trier_visiteurs(donnee)
        for visiteur in visiteurs:
            writer.writerow(visiteur)
    csvfile.close()

