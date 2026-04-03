from flask import Flask

from controllers.visiteurs_controller import visiteurs_controller
from controllers.config_controller import config_controller

app = Flask(__name__)


app.register_blueprint(visiteurs_controller)
app.register_blueprint(config_controller)

@app.route('/')
def hello_world():
    return 'CampusFlow'


if __name__ == '__main__':
    app.run()
