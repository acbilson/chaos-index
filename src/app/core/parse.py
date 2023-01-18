import os
import argparse
from urllib.parse import urljoin, urlparse
from collections import namedtuple

import sqlite3
from sqlite3 import Connection
from bs4 import BeautifulSoup, Tag


def get_db_path() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="path to the sqlite3 db file")
    args = parser.parse_args()
    return args.path


def connect(db_path: str) -> Connection:
    return sqlite3.connect(db_path)


def read_file(path: str) -> str:
    content = ""
    with open(path, "r") as f:
        content = f.read()
    return content


def get_title(page: BeautifulSoup, query: str) -> Tag:
    query_values = query.split('.')
    if len(query_values) == 2:
        tag, class_name = query_values
        return page.find(tag, class_=class_name).find_all('p')
    else:
        tag = query
        return page.find(tag)


def get_content(page: BeautifulSoup, query: str) -> list[Tag]:
    query_values = query.split('.')
    if len(query_values) == 2:
        tag, class_name = query_values
        return page.find(tag, class_=class_name).find_all('p')
    else:
        tag = query
        return page.find(tag).find_all('p')
