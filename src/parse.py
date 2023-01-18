import os
import argparse
from urllib.parse import urljoin, urlparse
from collections import namedtuple

import sqlite3
from sqlite3 import Connection
from bs4 import BeautifulSoup, Tag


Site = namedtuple('Site', 'id title_query content_query')
File = namedtuple('File', 'id link path site_id')


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
    for x in cur.execute("SELECT rowid, title_query, content_query FROM site"):
        sites.append(Site(x[0], x[1], x[2]))
    return sites


def get_files(con: Connection, site_id: int) -> list[File]:
    cur = con.cursor()
    files = []
    for x in cur.execute(f"SELECT rowid, url, path, site_id FROM file WHERE site_id == ?", (str(site_id))):
        files.append(File(x[0], x[1], x[2], x[3]))
    return files


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


def insert_metadata(con: Connection, title: Tag, content: list[Tag], file_id: int) -> None:
    data = (title.getText(), ''.join([x.getText() for x in content]), str(file_id))
    cur = con.cursor()
    cur.execute("INSERT INTO metadata VALUES (?, ?, ?)", data)
    con.commit()


if __name__ == "__main__":
    path = get_db_path()
    con = connect(path)
    sites = get_sites(con)

    for site in sites:
        files = get_files(con, int(site.id))
        for file in files:
            data = read_file(file.path)
            page = BeautifulSoup(data, 'html.parser')
            title = get_title(page, site.title_query)
            content = get_content(page, site.content_query)
            insert_metadata(con, title, content, file.id)
