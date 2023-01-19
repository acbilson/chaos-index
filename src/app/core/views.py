import os
from datetime import datetime, timedelta
import json
import requests
from http import HTTPStatus
from flask import jsonify
from flask import current_app as app
from bs4 import BeautifulSoup
from ..core import core_bp

from app.core import proxy, scrape, parse, index
from app.extensions import cache


@core_bp.route("/index", methods=["GET"])
# TODO: make sure connection closes before any return (convert to with proxy:)
# TODO: move path information to config object
@cache.cached(timeout=300)
def build_index():
    """
    Performs a multi-step process to create an index from multiple websites.

    Step 1. Scrape a table of websites for pages and store them to disk
    Step 2. Parse each HTML file for indexable metadata
    Step 3. Convert metadata to index.json
    """
    con = proxy.connect(app.config["DB_PATH"])

    # TODO: read site config from a /mnt TOML file that I could deploy w/ Ansible
    sites = proxy.read_sites(con)

    if not sites or len(sites) == 0:
        return jsonify(msg="No sites available for scraping. Aborting")

    for site in sites:

        ## STEP 1. Scrape
        #################
        # TODO: simplify this scraper with a top-level config. Should just return file objects
        page = scrape.get_landing_page(site.url)
        link_tags = scrape.query_link_tags(page, site.link_query)
        links = scrape.get_links(link_tags, site.partial_links == '1', site.url)
        files = scrape.get_files(int(site.id), site.author, links)
        scrape.create_root_path(site.author)

        for file in files:
            if not os.path.exists(scrape.get_full_path(file)) and not proxy.file_in_db(con, file):
                scrape.write_file(file)
                proxy.create_file(con, file)

        ## Step 2: Parse
        ################
        # TODO: simplify further, taking file objects and returning metadata
        files = proxy.read_files(con, int(site.id))
        for file in files:
            data = parse.read_file(file.path)
            page = BeautifulSoup(data, 'html.parser')
            title = parse.get_title(page, site.title_query)
            content = parse.get_content(page, site.content_query)
            proxy.create_metadata(con, title, content, file.id)

        ## Step 3: Index
        ################
        # TODO: a fairly simple step. clarify
        metadatas = proxy.read_metadatas(con)
        return jsonify(index.save_index(metadatas))

