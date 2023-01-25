import os
from .init import init_db
from .proxy import SqlProxy
from .models import Site, File, Metadata


class SqlProxyExtension:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        db_path = os.path.join(app.config["DB_PATH"], "data.db")
        init_db(db_path)
        app.extensions["db"] = SqlProxy(db_path)
