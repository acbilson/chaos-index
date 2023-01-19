from os import environ


class BaseConfig(object):
    """Set Flask configuration variables"""

    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 5000
    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    SITE = environ.get("SITE") or "https://index.alexbilson.dev"
    DB_PATH = environ.get("DB_PATH") or "/mnt/db/data.db"
    SHARE_PATH = environ.get("SHARE_PATH") or "/mnt/share"

    FLASK_SECRET_KEY = environ.get("FLASK_SECRET_KEY")
    SESSION_SECRET = environ.get("SESSION_SECRET")

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300


class TestConfig(object):
    """Set Flask test configuration variables"""

    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 80
    FLASK_ENV = "development"
    SITE = "http://localhost/"
    DB_PATH = "/mnt/db/data.db"
    SHARE_PATH = "/mnt/share"

    FLASK_SECRET_KEY = "my secret test key"
    SESSION_SECRET = "my secret test session"

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
