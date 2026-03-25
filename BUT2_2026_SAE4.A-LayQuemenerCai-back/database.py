import sqlite3
from flask import g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.sqlite3')
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
