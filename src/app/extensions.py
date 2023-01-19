from flask_caching import Cache
from app.proxy import SqlProxyExtension

cache = Cache()
db = SqlProxyExtension()
