import os
from os import environ
from datetime import date
import logging
from itertools import groupby

from app.proxy import SqlProxy
from app.proxy import init_db
import app.ops as ops


# TODO: batch jobs for less memory usage per run. I think this
# is why it's failing on Vultr
def build_index(db_path: str, share_path: str, log_path):
    """
    Performs a two-step process to create an index from multiple websites.

    Step 1. Scrape a table of websites for pages and store them to disk
    Step 2. Parse each HTML file for indexable metadata
    """
    # configures logging
    logging.basicConfig(
        filename=os.path.join(log_path, "build_index.log"), level=logging.INFO
    )

    logging.info("==================\nSTARTING INDEX JOB\n==================")
    logging.info(date.today())
    logging.info("db path: %s", db_path)
    logging.info("share path: %s", share_path)

    # instantiates the database if it doesn't exist
    init_db(db_path)
    logging.info("initiated database")

    db = SqlProxy(db_path)
    db.connect()
    logging.info("connected to db at %s", db_path)

    sites = db.read_sites()

    if not sites or len(sites) == 0:
        logging.info("No sites available for scraping.")
        return

    ## Step 1: Scrape
    #################
    for site in sites:
        ops.create_root_dir(share_path, site.author)
        files = ops.scrape_site(site, share_path)
        missing_files = [f for f in files if not os.path.exists(f.path)]
        missing_files_in_db = [f for f in files if not db.file_in_db(f)]

        logging.info("scraping %s", site.url)
        logging.info("Number of files to download: %s", len(missing_files))
        logging.info("Number of files to enter into db: %s", len(missing_files_in_db))

        # TODO: make async
        if len(missing_files) > 0:
            for file in missing_files:
                page_html = ops.scrape_page(file.url)
                logging.info("Downloading %s", file.url)
                ops.write_file(file.path, page_html)

        if len(missing_files_in_db) > 0:
            logging.info("Inserting %s files into db", len(files))
            db.create_files(missing_files_in_db)

    ## Step 2: Parse
    ################
    logging.info("Getting metadata")
    files = db.read_files_without_metadata()
    logging.info("Number of files without metadata: %s", len(files))

    for site_id, file_group in groupby(files, lambda x: x.site_id):
        site = list(filter(lambda s: s.id == site_id, sites))[0]
        logging.info("Parsing metadata for %s", site.url)
        metadatas = []
        for file in file_group:
            page_html = ops.read_file(file.path)
            metadata = ops.parse_metadata(site, page_html, file)
            metadatas.append(metadata)

        if len(metadatas) > 0:
            logging.info("Inserting %s metadata for %s", len(metadatas), site.url)
            db.create_metadatas(site_id, metadatas)

    db.disconnect()
    logging.info("database connection closed")


if __name__ == "__main__":
    share_path = environ.get("SHARE_PATH") or "/mnt/index/share"
    db_path = os.path.join(environ.get("DB_PATH") or "/mnt/index/db", "data.db")
    log_path = environ.get("LOG_PATH") or "/mnt/index/logs"
    build_index(db_path, share_path, log_path)
