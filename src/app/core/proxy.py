import sqlite3
from sqlite3 import Connection
from app.core.models import Site, File


def connect(db_path: str) -> Connection:
    return sqlite3.connect(db_path)


def file_in_db(con: Connection, file: File) -> bool:
    cur = con.cursor()
    return cur.execute(f"SELECT * FROM file WHERE url == '{file.link}'").fetchone is not None


def read_sites(con: Connection) -> list[Site]:
    cur = con.cursor()
    sites = []
    for x in cur.execute("SELECT rowid, author, url, partial_links, link_query, title_query, content_query FROM site;"):
        sites.append(Site(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    return sites


def create_file(con: Connection, file: File) -> None:
    to_insert = (file.link, get_full_path(file), file.site_id)
    cur = con.cursor()
    cur.execute("INSERT INTO file VALUES (?, ?, ?, CURRENT_DATE)", to_insert)
    con.commit()


def read_files(con: Connection, site_id: int) -> list[File]:
    cur = con.cursor()
    files = []
    for x in cur.execute(f"SELECT rowid, url, path, site_id FROM file WHERE site_id == ?", (str(site_id))):
        files.append(File(x[0], x[1], x[2], x[3]))
    return files


def create_metadata(con: Connection, title: Tag, content: list[Tag], file_id: int) -> None:
    data = (title.getText(), ''.join([x.getText() for x in content]), str(file_id))
    cur = con.cursor()
    cur.execute("INSERT INTO metadata VALUES (?, ?, ?)", data)
    con.commit()


def read_metadatas(con: Connection) -> list[Metadata]:
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

