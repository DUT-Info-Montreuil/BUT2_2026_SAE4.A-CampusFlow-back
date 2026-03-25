from flask import Blueprint, jsonify, request, Response
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


@visiteurs_controller.route('/<int:id_visiteur>', methods=['DELETE'])
def delete_visiteur_by_id(id_visiteur: int):
    name = service_visiteurs.delete_visiteur_by_id(id_visiteur)
    if name is not None:
        return jsonify(f"Le visiteur {name} a été supprimé avec succès"), 204
    else:
        return jsonify("Suppression des visiteurs échoué"), 404


@visiteurs_controller.route('/<int:id_visiteur>', methods=['PUT'])
def modif_visiteurs(id_visiteur: int):
    data = request.get_json()
    try:
        service_visiteurs.modif_visiteur(id_visiteur, data)
        return jsonify("Visiteur modifié"), 201
    except Exception as exception:
        return jsonify(f"{exception}"), 404
