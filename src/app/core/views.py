import os
from os import path
from datetime import datetime, timedelta
import json
import requests
from http import HTTPStatus
from flask import Response, request, render_template, url_for, redirect, jsonify
from flask import current_app as app
from ..core import core_bp

@core_bp.route("/index", methods=["GET"])
def build_index():
    pass
