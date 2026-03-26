import os
from genericpath import exists

from flask import Blueprint, jsonify, request, send_file
import services.visiteurs_service as service_visiteurs

visiteurs_controller = Blueprint('visiteurs', __name__, url_prefix='/visiteurs')


@visiteurs_controller.route('', methods=['GET'])
def get_visiteurs():
    visiteurs = service_visiteurs.get_all()
    return jsonify(visiteurs), 200


@visiteurs_controller.route('/<int:id>', methods=['GET'])
def get_visiteur_by_id(id):
    visiteur = service_visiteurs.get_visiteur_by_id(id)
    if visiteur is None:
        return jsonify("Visiteur introuvable"), 404
    return jsonify(visiteur), 200


@visiteurs_controller.route('', methods=['POST'])
def add_visiteurs():
    data = request.get_json()
    try:
        service_visiteurs.add_visiteur(data)
        return jsonify("Visiteur ajouté"), 201
    except Exception as exception:
        return jsonify(f"{exception}"), 404


@visiteurs_controller.route('', methods=['DELETE'])
def delete_visiteurs():
    count = service_visiteurs.delete_all()
    if count > 0:
        return jsonify(f"{count} visiteurs ont été supprimés de la base de données"), 204
    else:
        return jsonify("Suppression des visiteurs échoué"), 404

@visiteurs_controller.route('/export', methods=['POST']) #verifier si utiliser post
def export_visiteurs():
    if not exists("temporaire"):
        os.mkdir("temporaire")
    data = request.get_json()
    service_visiteurs.fichier_csv(data)
    return send_file("temporaire/visiteurs.csv",mimetype="text/csv"),200