from database import get_db


def get_allRepository():
    db = get_db()
    cursor = db.execute("SELECT * FROM visiteurs")
    return cursor.fetchall()


def get_visiteurRepository(id_visiteur):
    db = get_db()
    cursor = db.execute("SELECT * FROM visiteurs WHERE id=?", (id_visiteur,))
    return cursor.fetchone()


def add_visiteurRepository(visiteur, formation_intitule, formation_niveau):
    db = get_db()
    db.execute("""
            INSERT INTO visiteurs (
                nom, prenom, email, telephone, date_de_naissance, ville, code_postal,
                nom_lycee, code_postal_lycee, bac_intitule, bac_annee, bac_matiere1, bac_matiere2,
                formation_actuelle_intitule, formation_actuelle_niveau, handicap, reorientation, immersion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
        visiteur.nom,
        visiteur.prenom,
        visiteur.email,
        visiteur.telephone,
        str(visiteur.date_naissance),
        visiteur.adresse.ville,
        visiteur.adresse.codePostal,
        visiteur.lycee.nom_lycee,
        visiteur.lycee.codePostal,
        visiteur.bac.intitule,
        visiteur.bac.annee,
        visiteur.bac.matiere1,
        visiteur.bac.matiere2,
        formation_intitule,
        formation_niveau,
        visiteur.options.handicap,
        visiteur.options.reorientation,
        visiteur.options.immersion
    ))
    db.commit()


def update_visiteurRepository(id_visiteur, visiteur, formation_intitule, formation_niveau, handicap, reorientation,
                              immersion):
    db = get_db()
    db.execute("""
            UPDATE visiteurs
            SET nom= ?,
                prenom= ?,
                email= ?,
                telephone= ?,
                date_de_naissance= ?,
                ville= ?,
                code_postal= ?,
                nom_lycee= ?,
                code_postal_lycee= ?,
                bac_intitule= ?,
                bac_annee= ?,
                bac_matiere1= ?,
                bac_matiere2= ?,
                formation_actuelle_intitule= ?,
                formation_actuelle_niveau= ?,
                handicap= ?,
                reorientation= ?,
                immersion= ?,
            WHERE id=?;
        """, (visiteur.nom, visiteur.prenom, visiteur.email, visiteur.telephone, str(visiteur.date_naissance),
              visiteur.adresse.ville, visiteur.adresse.codePostal, visiteur.lycee.nom_lycee, visiteur.lycee.codePostal,
              visiteur.bac.intitule, visiteur.bac.annee, visiteur.bac.matiere1, visiteur.bac.matiere2,
              formation_intitule,
              formation_niveau, handicap, reorientation, immersion, id_visiteur,))
    db.commit()


def delete_visiteurRepository(id_visiteur):
    db = get_db()
    name = None
    name = db.execute("SELECT nom FROM visiteurs WHERE id= ?", (id_visiteur,))
    db.commit()
    nameF = name.fetchone()
    cursor = db.execute("DELETE FROM visiteurs WHERE id=?", (id_visiteur,))
    db.commit()
    return nameF


def appelle_visiteurs_filtreRepository(filtre):
    db = get_db()
    cursor = db.execute(
        "SELECT * FROM visiteurs WHERE (nom = :nom OR :nom IS NULL) AND (prenom = :prenom OR :prenom IS NULL) "
        "AND (email = :email OR :email IS NULL) AND (ville = :ville OR :ville IS NULL) AND (bac_intitule = :bac_intitule OR :bac_intitule IS NULL) "
        "AND (nom_lycee = :nom_lycee OR :nom_lycee IS NULL) AND (reorientation = :reorientation OR :reorientation IS NULL) "
        "AND (immersion = :immersion OR :immersion IS NULL) AND (handicap = :handicap OR :handicap IS NULL) "
        "AND (formation_actuelle_intitule = :formation_actuelle_intitule OR :formation_actuelle_intitule IS NULL)"
        "order by nom",
        filtre)
    return cursor.fetchall()


def delete_allRepository():
    db = get_db()
    cursor = db.execute("DELETE FROM visiteurs")
    cursor2 = db.execute("DELETE FROM sqlite_sequence where name=?", ('visiteurs',))  # Reset l'id à 0
    db.commit()
    return cursor


def stat_bacRepository():
    db = get_db()
    cursor = db.execute("select bac_intitule,count(*) from visiteurs group by bac_intitule")
    return cursor.fetchall()


def stat_reorientationRepository():
    db = get_db()
    cursor = db.execute("select reorientation,count(*) from visiteurs group by reorientation")
    return cursor.fetchall()


def stat_immersionRepository():
    db = get_db()
    cursor = db.execute("select immersion,count(*) from visiteurs group by immersion")
    return cursor.fetchall()


def stat_handicapRepository():
    db = get_db()
    cursor = db.execute("select handicap,count(*) from visiteurs group by handicap")
    return cursor.fetchall()
