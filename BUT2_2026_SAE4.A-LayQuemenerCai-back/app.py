from flask import Flask

from controllers.visiteurs_controller import visiteurs_controller

app = Flask(__name__)


app.register_blueprint(visiteurs_controller)


@app.route('/')
def hello_world():
    return 'CampusFlow'


if __name__ == '__main__':
    app.run()
