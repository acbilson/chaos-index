import os
import json
import argparse
from urllib.parse import urljoin, urlparse
from collections import namedtuple

import sqlite3
from sqlite3 import Connection


Metadata = namedtuple('Metadata', 'url author title content')


def get_db_path() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="path to the sqlite3 db file")
    args = parser.parse_args()
    return args.path


def connect(db_path: str) -> Connection:
    return sqlite3.connect(db_path)


def get_metadatas(con: Connection) -> list[Metadata]:
    cur = con.cursor()
    metadata = []
    for x in cur.execute("""
        SELECT f.url, author, title, content
        FROM metadata m
        join file f on m.file_id = f.rowid
        join site s on f.site_id = s.rowid;
        """):
        metadata.append(Metadata(x[0], x[1], x[2], x[3]))
    return metadata


def save_index(data: list[Metadata]) -> None:
    content = []
    for metadata in metadatas:
        content.append(dict(id=metadata.url, author=metadata.author, title=metadata.title, content=metadata.content))

    path = os.path.join('dist', 'index.json')
    with open(path, 'w') as f:
        f.write(json.dumps(content))


if __name__ == "__main__":
    path = get_db_path()
    con = connect(path)
    metadatas = get_metadatas(con)
    save_index(metadatas)
