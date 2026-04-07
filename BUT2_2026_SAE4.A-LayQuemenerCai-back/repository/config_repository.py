from database import get_db


def get_evenement_allRepository():
    db = get_db()
    cursor = db.execute("SELECT * FROM evenements")
    return cursor.fetchall()


def add_evenementRepository(evenement):
    db = get_db()
    db.execute("""
        INSERT INTO evenements (intitule,ville,code_postal,date)
        VALUES (?,?,?,?)""", (
        evenement.intitule,
        evenement.lieu.ville,
        evenement.lieu.codePostal,
        evenement.date
    ))
    db.commit()


def delete_evenement_allRepository():
    db = get_db()
    cursor = db.execute("DELETE FROM evenements")
    cursor2 = db.execute("DELETE FROM sqlite_sequence where name=?", ('evenement',))  # Reset l'id à 0
    db.commit()
    return cursor


def delete_evenement_by_idRepository(id_evenement):
    db = get_db()
    name = None
    name = db.execute("SELECT intitule FROM evenements WHERE id= ?", (id_evenement,))
    db.commit()
    nameF = name.fetchone()
    cursor = db.execute("DELETE FROM evenements WHERE id=?", (id_evenement,))
    db.commit()
    return nameF


def modif_evenementRepository(id_evenement, evenement):
    db = get_db()
    db.execute("""
        UPDATE evenement
        SET intitule= ?,
            lieu= ?
        WHERE id= ?;""", (
        evenement.intitule,
        evenement.lieu,
        id_evenement
    ))
    db.commit()


def get_formation_allRepository():
    db = get_db()
    cursor = db.execute("SELECT * FROM formations_iut")
    return cursor.fetchall()


def add_formationRepository(formation):
    db = get_db()
    db.execute("""
        INSERT INTO formations_iut (intitule,domaine)
        VALUES (?,?)""", (
        formation.intitule,
        formation.domaine
    ))
    db.commit()


def delete_formation_allRepository():
    db = get_db()
    cursor = db.execute("DELETE FROM formations_iut")
    cursor2 = db.execute("DELETE FROM sqlite_sequence where name=?", ('formation',))  # Reset l'id à 0
    db.commit()
    return cursor


def delete_formation_by_idRepository(id_formation):
    db = get_db()
    name = None
    name = db.execute("SELECT intitule FROM formations_iut WHERE id= ?", (id_formation,))
    db.commit()
    nameF = name.fetchone()
    cursor = db.execute("DELETE FROM formations_iut WHERE id=?", (id_formation,))
    db.commit()
    return nameF


def modif_formationRepository(id_formation, formation):
    db = get_db()
    db.execute("""
        UPDATE formation
        SET intitule= ?,
            lieu= ?
        WHERE id= ?;""", (
        formation.intitule,
        formation.lieu,
        id_formation
    ))
    db.commit()