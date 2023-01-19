import sqlite3
from sqlite3 import Connection


def connect(db_path: str) -> Connection:
    return sqlite3.connect(db_path)


def create_tables(con: Connection) -> None:
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
    CREATE TABLE IF NOT EXISTS metadata(
        title TEXT NULL,
        content TEXT NULL,
        file_id INTEGER NOT NULL,
        FOREIGN KEY (file_id)
            REFERENCES file (rowid));
    """)


def insert(con: Connection, sql: str) -> None:
    cur = con.cursor()
    cur.execute(sql)
    con.commit()


def remove_defaults(con: Connection) -> None:
    cur = con.cursor()
    cur.execute("DELETE FROM site;")


def insert_defaults(con: Connection) -> None:
        insert(con, """
        INSERT INTO site VALUES
            ('Maggie Appleton', 'https://maggieappleton.com/notes', 1, 'section', 'h1', 'main'),
            ('Alex Bilson', 'https://alexbilson.dev/plants', 0, 'ul.fill-list', 'h1', 'article.e-content');
""")


def init_db(db_path: str) -> None:
    con = connect(db_path)
    create_tables(con)
    remove_defaults(con)
    insert_defaults(con)
    con.close()
