from flask import Blueprint, jsonify, request, Response
import services.visiteurs_service as service_visiteurs

visiteurs_controller = Blueprint('visiteurs', __name__, url_prefix='/visiteurs')


@visiteurs_controller.route('', methods=['GET'])
def get_visiteurs():
    nom = request.args.get('nom')
    prenom = request.args.get('prenom')
    telephone = request.args.get('telephone')
    email = request.args.get('email')
    ville = request.args.get('ville')
    bac = request.args.get('bac')
    lycee = request.args.get('lycee')
    reorientation = request.args.get('reorientation')
    immersion = request.args.get('immersion')
    handicap = request.args.get('handicap')
    formation_actuelle = request.args.get('formation_actuelle')
    limit = request.args.get('limit', default=5, type=int)
    page = request.args.get('page', default=1, type=int)

    filtres = dict()
    if nom:
        filtres['nom'] = nom
    if prenom:
        filtres['prenom'] = prenom
    if telephone:
        filtres['telephone'] = telephone
    if email:
        filtres['email'] = email
    if lycee:
        filtres['nom_lycee'] = lycee
    if ville:
        filtres['ville'] = ville
    if bac:
        filtres['bac_intitule'] = bac
    if reorientation:
        if reorientation.lower() == 'true':
            filtres['reorientation'] = 1
        else:
            filtres['reorientation'] = 0
    if handicap:
        if handicap.lower() == 'true':
            filtres['handicap'] = 1
        else:
            filtres['handicap'] = 0
    if immersion:
        if handicap.lower() == 'true':
            filtres['immersion'] = 1
        else:
            filtres['immersion'] = 0
    if formation_actuelle:
        filtres['formation_actuelle_intitule'] = formation_actuelle

    if filtres:
        visiteurs = service_visiteurs.get_all(filtres, limit, page)
    else:
        visiteurs = service_visiteurs.get_all(None, limit, page)
    return jsonify({'data': visiteurs, 'page': page, 'limit': limit}), 200


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
        return jsonify(f"Problème?{exception}"), 404


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


@visiteurs_controller.route('/export', methods=['GET'])
def export_visiteurs():
    if not exists("temporaire"):
        os.mkdir("temporaire")
    service_visiteurs.fichier_csv()
    return send_file("temporaire/visiteurs.csv", mimetype="text/csv"), 200


@visiteurs_controller.route('/stat', methods=['GET'])
def stat_visiteurs():
    visiteurs = service_visiteurs.statistique_visiteurs()
    return jsonify(visiteurs), 200


@visiteurs_controller.route('/stat/bac', methods=['GET'])
def stat_bac_visiteurs():
    visiteurs = service_visiteurs.stat_bac()
    return jsonify(visiteurs), 200


@visiteurs_controller.route('/stat/handicap', methods=['GET'])
def stat_handicap_visiteurs():
    visiteurs = service_visiteurs.stat_handicap()
    return jsonify(visiteurs), 200


@visiteurs_controller.route('/stat/immersion', methods=['GET'])
def stat_immersion_visiteurs():
    visiteurs = service_visiteurs.stat_immersion()
    return jsonify(visiteurs), 200


@visiteurs_controller.route('/stat/reorientation', methods=['GET'])
def stat_reorientation_visiteurs():
    visiteurs = service_visiteurs.stat_reorientation()
    return jsonify(visiteurs), 200
