import os
from flask import Flask, render_template
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig, TestingConfig
from application.data.database import db
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application.data.models import User, Role
from flask_login import LoginManager
from flask_security import utils
from flask_sse import sse
from flask_cors import CORS

app = None
api = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    CORS(app)

    if os.getenv('ENV', "development") == "development":
        app.config.from_object(LocalDevelopmentConfig)
    elif os.getenv('ENV', "development") == 'testing':
        app.config.from_object(TestingConfig)

    db.init_app(app)
    app.app_context().push()
    api = Api(app)
    app.app_context().push()

    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)

    return app, api

app, api = create_app()

from application.controller.controllers import *
from application.controller.api import UserAPI, TrackerAPI, TrackerLogAPI

api.add_resource(UserAPI, "/api/user")
api.add_resource(TrackerAPI, "/api/tracker")
api.add_resource(TrackerLogAPI, "/api/tracker/log")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def not_authorized(e):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)