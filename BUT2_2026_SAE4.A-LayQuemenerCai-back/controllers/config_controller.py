import os
from genericpath import exists

from flask import Blueprint, jsonify, request, send_file
import services.config_service as service_config

config_controller = Blueprint('config', __name__, url_prefix='/config')


@config_controller.route('/evenement',methods=["GET"])
def get_evenements():
    data = service_config.get_evenement_all()
    if data is None:
        return jsonify('Evenements introuvable'), 404
    return jsonify(data), 200


@config_controller.route('/evenement', methods=["POST"])
def add_evenements():
    data = request.get_json()
    try:
        service_config.add_evenement(data)
        return jsonify("Evènement ajouté"), 201
    except Exception as exception:
        return jsonify(f"{exception}"), 404


@config_controller.route('/evenement', methods=['DELETE'])
def delete_evenement():
    count = service_config.delete_evenement_all()
    if count > 0:
        return jsonify(f"{count} évènement ont été supprimés de la base de données"), 204
    else:
        return jsonify("Suppression des évènements échoué"), 404


@config_controller.route('/evenement/<int:id_evenement>', methods=['DELETE'])
def delete_evenement_by_id(id_evenement: int):
    name = service_config.delete_evenement_by_id(id_evenement)
    if name is not None:
        return jsonify(f"L'évènement {name} a été supprimé avec succès"), 204
    else:
        return jsonify("Suppression de l'évènement échoué"), 404


@config_controller.route('/evenement/<int:id_evenement>', methods=['PUT'])
def modif_evenement(id_evenement: int):
    data = request.get_json()
    try:
        service_config.modif_evenement(id_evenement, data)
        return jsonify("Evènement modifié"), 201
    except Exception as exception:
        return jsonify(f"{exception}"), 404


@config_controller.route('/formation',methods=["GET"])
def get_formations():
    data = service_config.get_formation_all()
    if data is None:
        return jsonify('Formation introuvable'), 404
    return jsonify(data), 200


@config_controller.route('/formation', methods=["POST"])
def add_formations():
    data = request.get_json()
    try:
        service_config.add_formation(data)
        return jsonify("Formation ajouté"), 201
    except Exception as exception:
        return jsonify(f"{exception}"), 404


@config_controller.route('/formation', methods=['DELETE'])
def delete_formation():
    count = service_config.delete_formation_all()
    if count > 0:
        return jsonify(f"{count} formation ont été supprimés de la base de données"), 204
    else:
        return jsonify("Suppression des formations échoué"), 404


@config_controller.route('/formation/<int:id_formation>', methods=['DELETE'])
def delete_formation_by_id(id_formation: int):
    name = service_config.delete_formation_by_id(id_formation)
    if name is not None:
        return jsonify(f"La formation {name} a été supprimé avec succès"), 204
    else:
        return jsonify("Suppression de la formation échoué"), 404


@config_controller.route('/formation/<int:id_formation>', methods=['PUT'])
def modif_formation(id_formation: int):
    data = request.get_json()
    try:
        service_config.modif_formation(id_formation, data)
        return jsonify("Evènement modifié"), 201
    except Exception as exception:
        return jsonify(f"{exception}"), 404