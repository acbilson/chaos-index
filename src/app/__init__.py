import logging
from flask import Flask, Response
from flask_cors import CORS

from app import config
from app.core import core_bp
from . import init_db


def create_app(config=config.BaseConfig):
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    cors = CORS(app)
    app.config.from_object(config)

    app.logger.info(app.config.get("DB_PATH"))

    # required to encrypt session
    app.secret_key = app.config["FLASK_SECRET_KEY"]

    with app.app_context():

        # register blueprints
        app.register_blueprint(core_bp)

        # initiate db
        init_db(app.config["DB_PATH"])

        @app.route("/healthcheck", methods=["GET"])
        def health():
            return Response(status=200)

        return app
