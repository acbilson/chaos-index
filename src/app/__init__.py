import logging
from flask import Flask, Response
from flask_cors import CORS

from app import config
from app.core import core_bp
from app.extensions import cache, db

def create_app(config=config.BaseConfig):
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)
    cors = CORS(app)

    app.logger.info(app.config.get("DB_PATH"))

    # required to encrypt session
    app.secret_key = app.config["FLASK_SECRET_KEY"]

    with app.app_context():

        # register blueprints
        app.register_blueprint(core_bp)

        # register extensions
        cache.init_app(app)
        db.init_app(app)


        @app.before_request
        def before_request():
            app.extensions["db"].connect()


        @app.after_request
        def after_request(resp):
            app.extensions["db"].disconnect()
            return resp


        @app.route("/healthcheck", methods=["GET"])
        def health():
            return Response(status=200)

        return app
