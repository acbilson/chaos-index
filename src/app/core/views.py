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
    query = request.args.get("q")

    if query is None:
        return jsonify(
            success=False,
            message="No query entered. Please add a ?q=search_string parameter.",
        )

    db: SqlProxy = app.extensions["db"]

    metadatas, msg = db.query_metadata(query)

    if msg != "":
        return jsonify(success=False, message=f"search failed: {msg}")

    content = []
    for metadata in metadatas:
        content.append(
            dict(
                id=metadata.url,
                author=metadata.author,
                title=metadata.title,
                content=metadata.content,
            )
        )

    return jsonify(success=True, message="", content=content)


@core_bp.route("/sites", methods=["GET"])
# TODO: add logging
def sites():
    """
    Returns the sites which have been indexed, along with the page count

    returns: dict(author, url, pages)
    """
    db: SqlProxy = app.extensions["db"]

    content, msg = db.read_sites_with_page_count()

    if msg != "":
        return jsonify(success=False, message=f"site retrieval failed: {msg}")

    return jsonify(success=True, message="", content=content)
