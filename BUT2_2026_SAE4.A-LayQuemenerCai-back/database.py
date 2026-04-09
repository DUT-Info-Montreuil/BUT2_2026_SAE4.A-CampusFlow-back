import os
import sqlite3
from flask import g
from flask.cli import load_dotenv


def get_db():
    load_dotenv()
    if 'db' not in g:
        g.db = sqlite3.connect(os.getenv('DATABASE'))
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
