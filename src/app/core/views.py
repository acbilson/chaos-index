import os
from datetime import datetime, timedelta
import json
import requests
from http import HTTPStatus
from flask import jsonify
from flask import current_app as app
from bs4 import BeautifulSoup
from ..core import core_bp

from app.extensions import cache
from app.proxy import SqlProxy
import app.ops as ops


@core_bp.route("/index", methods=["GET"])
# TODO: add logging
@cache.cached()
def build_index():
    """
    Performs a multi-step process to create an index from multiple websites.

    Step 1. Scrape a table of websites for pages and store them to disk
    Step 2. Parse each HTML file for indexable metadata
    Step 3. Convert metadata to index.json
    """
    db: SqlProxy = app.extensions["db"]
    sites = db.read_sites()

    if not sites or len(sites) == 0:
        return jsonify(msg="No sites available for scraping. Aborting")

    ## Step 1: Scrape
    #################
    for site in sites:
        ops.create_root_dir(app.config['SHARE_PATH'], site.author)
        files = ops.scrape_site(site, app.config['SHARE_PATH'])
        missing_files = [f for f in files if not os.path.exists(f.path)]
        missing_files_in_db = [f for f in files if not db.file_in_db(f)]

        # TODO: make async
        for file in missing_files:
            page_html = ops.scrape_page(file.url)
            ops.write_file(file.path, page_html)

        db.create_files(missing_files_in_db)

    ## Step 2: Parse
    ################
    for site in sites:
        files = db.read_files_without_metadata(site.id)
        metadatas = []

        for file in files:
            page_html = ops.read_file(file.path)
            metadata = ops.parse_metadata(site, page_html, file)
            metadatas.append(metadata)

        db.create_metadatas(metadatas)

    ## Step 3: Index
    ################
    metadatas = db.read_metadatas()

    content = []
    for metadata in metadatas:
        content.append(dict(id=metadata.url, author=metadata.author, title=metadata.title, content=metadata.content))

    return jsonify(content)

