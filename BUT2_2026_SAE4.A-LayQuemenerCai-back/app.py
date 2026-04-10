from dotenv import load_dotenv

load_dotenv()
from flask import Flask
from flask_cors import CORS
from controllers.visiteurs_controller import visiteurs_controller
from controllers.config_controller import config_controller
from init_db import init_db
import os

app = Flask(__name__)
CORS_URL = os.getenv("CORS_ORIGIN")
CORS(app, origins=CORS_URL)

app.register_blueprint(visiteurs_controller)
app.register_blueprint(config_controller)

init_db()


@app.route('/')
def hello_world():
    return 'CampusFlow'


if __name__ == '__main__':
    app.run()
