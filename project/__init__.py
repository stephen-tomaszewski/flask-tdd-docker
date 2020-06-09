import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# instantiate the db
# https://flask.palletsprojects.com/en/1.1.x/extensiondev/
# Using this design pattern, no application-specific state is stored on the extension object, so one extension object
# can be used for multiple apps
db = SQLAlchemy()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    # all flask extensions must support factory pattern
    db.init_app(app)

    # register blueprintss
    from project.api.ping import ping_blueprint
    from project.api.users import users_blueprint

    app.register_blueprint(ping_blueprint)
    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
