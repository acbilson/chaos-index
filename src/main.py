from urllib.parse import urlparse
from app import create_app

app = create_app()

debug = app.config["FLASK_DEBUG"]
site = app.config["SITE"]
host = app.config["FLASK_HOST"]
port = app.config["FLASK_PORT"]

app.logger.info(f"View the site at {site}")

if __name__ == "__main__":
    app.run(host=host, port=port, debug=debug)
