import os
import json
import argparse
from urllib.parse import urljoin, urlparse
from collections import namedtuple

import sqlite3
from sqlite3 import Connection
from bs4 import BeautifulSoup, Tag
import requests

from app.core.models import File


def get_landing_page(url: str) -> BeautifulSoup:
    resp = requests.get(url)
    return BeautifulSoup(resp.content, 'html.parser') if resp.status_code == 200 else None


def query_link_tags(page: BeautifulSoup, query: str) -> list[Tag]:
    query_values = query.split('.')
    if len(query_values) == 2:
        tag, class_name = query_values
        return page.find(tag, class_=class_name).find_all('a')
    else:
        tag = query
        return page.find(tag).find_all('a')


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


def create_root_path(author: str) -> None:
    root = author.lower().replace(' ', '-')
    path = os.path.join('share', root)
    if not os.path.exists(path):
            os.makedirs(path)


def get_full_path(file: File) -> str:
    return os.path.join('share', file.path + '.html')


def file_is_present(con: Connection, path: str) -> bool:
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM file WHERE url == '{file.link}'")
    return result is not None and os.path.exists(path)
