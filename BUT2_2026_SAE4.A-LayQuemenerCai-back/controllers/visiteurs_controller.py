from flask import Blueprint, jsonify
import services.visiteurs_service as service_visiteurs

visiteurs_controller = Blueprint('visiteurs_controller', __name__, url_prefix='/visiteurs')


@visiteurs_controller.route('', methods=['GET'])
def get_visiteurs():
    visiteurs = service_visiteurs.get_all()
    return jsonify(visiteurs), 200
