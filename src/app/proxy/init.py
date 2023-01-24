import sqlite3
from sqlite3 import Connection


def init_db(db_path: str) -> None:
    con = sqlite3.connect(db_path)
    _create_tables(con)
    con.close()


def _connect(db_path: str) -> Connection:
    return sqlite3.connect(db_path)


def _create_tables(con: Connection) -> None:
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS site(
        author TEXT NOT NULL,
        url TEXT NOT NULL,
        partial_links INTEGER NOT NULL,
        link_query TEXT NOT NULL,
        title_query TEXT NOT NULL,
        content_query TEXT NOT NULL
        );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS file(
        url TEXT NOT NULL,
        path TEXT NOT NULL,
        site_id INTEGER NOT NULL,
        created TEXT NOT NULL,
        FOREIGN KEY (site_id)
            REFERENCES site (rowid));
    """)
    cur.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS metadata
        USING fts5(file_id, title, content);
    """)
