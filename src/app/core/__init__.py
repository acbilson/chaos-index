from flask import Blueprint

core_bp = Blueprint("core_bp", __name__)

from . import views
