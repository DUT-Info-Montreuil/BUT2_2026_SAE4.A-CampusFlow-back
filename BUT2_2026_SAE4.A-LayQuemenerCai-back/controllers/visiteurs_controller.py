from flask import Blueprint, jsonify, request, Response
import services.visiteurs_service as service_visiteurs

visiteurs_controller = Blueprint('visiteurs', __name__, url_prefix='/visiteurs')
listeKey: [] = ['nom', 'prenom', 'email', 'telephone', 'date_naissance', 'ville', 'codePostal', 'nomLycée', 'intituléBAC', 'matière1', 'matière2', 'intituléActu', 'NiveauEtudeActu', 'intituléEvent', 'lieu', 'dateEvent', 'handicap', 'reorientation', 'immersion']


@visiteurs_controller.route('', methods=['GET'])
def get_visiteurs():
    visiteurs = service_visiteurs.get_all()
    return jsonify(visiteurs), 200


@visiteurs_controller.route('', methods=['POST'])
def add_visiteurs():
    global listeKey
    conforme = True
    data = request.get_json()
    clé = data.keys() #Permet de regarder toutes les clés de la requête
    index = 0
    for value in clé:
        if value not in listeKey:
            conforme = False
        index += 1
    if conforme:
        service_visiteurs.add_visiteur(data)
        return jsonify(data), 200
    return jsonify('Erreur'), 400


@visiteurs_controller.route('', methods=['DELETE'])
def reset_visiteurs():
    service_visiteurs.delete_visiteurs()
    return jsonify("All Deleted"), 205