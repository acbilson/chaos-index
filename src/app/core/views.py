import os
from datetime import datetime, timedelta
import json
import requests
from http import HTTPStatus
from flask import jsonify, request
from flask import current_app as app
from bs4 import BeautifulSoup
from ..core import core_bp

from app.proxy import SqlProxy
import app.ops as ops


@core_bp.route("/search", methods=["GET"])
# TODO: add logging
def search():
    """
    Queries my full-text search table for the match
    """
    query = request.args.get('q')

    if query is None:
        return jsonify(msg="No query entered. Please add a ?q=search_string parameter. Aborting.")

    db: SqlProxy = app.extensions["db"]

    metadatas = db.query_metadata(query)

    content = []
    for metadata in metadatas:
        content.append(dict(id=metadata.url, author=metadata.author, title=metadata.title, content=metadata.content))

    return jsonify(content)
