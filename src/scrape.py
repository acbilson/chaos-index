import os
import json
import argparse
from urllib.parse import urljoin, urlparse
from collections import namedtuple
from typing import Callable

import sqlite3
from sqlite3 import Connection
from bs4 import BeautifulSoup, Tag
import requests

Site = namedtuple('Site', 'id author url partial_links link_query')
File = namedtuple('File', 'link root stem site_id')


def get_db_path() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="path to the sqlite3 db file")
    args = parser.parse_args()
    return args.path


def connect(db_path: str) -> Connection:
    return sqlite3.connect(db_path)


def get_sites(con: Connection) -> list[Site]:
    cur = con.cursor()
    sites = []
    for x in cur.execute("SELECT rowid, author, url, link_query, partial_links FROM site;"):
        sites.append(Site(x[0], x[1], x[2], x[3], x[4]))
    return sites


def get_landing_page(url: str) -> str:
    resp = requests.get(url)
    return resp.content if resp.status_code == 200 else ""


def query_link_tags(page: str, query: str) -> list[Tag]:
    query_values = query.split('.')
    soup = BeautifulSoup(page, 'html.parser')
    if len(query_values) == 2:
        tag, class_name = query_values
        return soup.find(tag, class_=class_name).find_all('a')
    else:
        tag = query
        return soup.find(tag).find_all('a')


def get_links(tags: list[Tag], partial_links: bool, root_url: str) -> list[str]:
    if partial_links:
        return [urljoin(root_url, x.get('href')) for x in tags]
    else:
        return [x.get('href') for x in tags]


def get_files(site_id: int, author: str, links: list[str]) -> list[File]:
    data = []
    for link in links:
        root = author.lower().replace(' ', '-')
        stem = urlparse(link).path.strip('/').replace('/', '_')
        data.append(File(link, root, stem, site_id))
    return data


def create_root_path(root: str) -> None:
    path = os.path.join('share', root)
    if not os.path.exists(path):
            os.makedirs(path)


def get_full_path(file: File) -> str:
    return os.path.join('share', file.root, file.stem + '.html')

def file_is_present(con: Connection, path: str) -> bool:
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM file WHERE url == '{file.link}'")
    return result is not None and os.path.exists(path)


def create_file(file: File) -> None:
    resp = requests.get(file.link)
    if resp.status_code == 200:
        with open(get_full_path(file), 'w+') as f:
            f.write(resp.text)


def insert_file(con: Connection, file: File) -> None:
    to_insert = (file.link, get_full_path(file), file.site_id)
    cur = con.cursor()
    print(to_insert)
    cur.execute("INSERT INTO file VALUES (?, ?, ?, CURRENT_DATE)", to_insert)
    con.commit()


if __name__ == "__main__":
    path = get_db_path()
    con = connect(path)
    sites = get_sites(con)

    for site in sites:
        page = get_landing_page(site.url)
        link_tags = query_link_tags(page, site.link_query)
        links = get_links(link_tags, site.partial_links == '1', site.url)
        files = get_files(int(site.id), site.author, links)
        create_root_path(files[0].root)

        for file in files:
            if not file_is_present(con, get_full_path(file)):
                create_file(file)
                insert_file(con, file)
