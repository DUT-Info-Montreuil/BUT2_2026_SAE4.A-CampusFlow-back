from flask import Flask
from flask_cors import CORS
from controllers.visiteurs_controller import visiteurs_controller

app = Flask(__name__)
CORS(app)

app.register_blueprint(visiteurs_controller)


@app.route('/')
def hello_world():
    return 'CampusFlow'


if __name__ == '__main__':
    app.run()
