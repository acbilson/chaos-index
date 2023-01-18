import argparse
import sqlite3
from sqlite3 import Connection


def get_db_path() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="path to the sqlite3 db file")
    args = parser.parse_args()
    return args.path


def connect(db_path: str) -> Connection:
    return sqlite3.connect(db_path)


def create_tables(con: Connection) -> None:
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE site(
        author TEXT NOT NULL,
        url TEXT NOT NULL,
        link_query TEXT NOT NULL,
        partial_links INTEGER NOT NULL,
        content_query TEXT NULL);
    """)
    cur.execute("""
    CREATE TABLE file(
        url TEXT NOT NULL,
        path TEXT NOT NULL,
        site_id INTEGER NOT NULL,
        created TEXT NOT NULL,
        FOREIGN KEY (site_id)
            REFERENCES site (rowid));
    """)

def insert(con: Connection, sql: str) -> None:
    cur = con.cursor()
    cur.execute(sql)
    con.commit()

def insert_defaults(con: Connection) -> None:
        insert(con, """
        INSERT INTO site VALUES
            ('Maggie Appleton', 'https://maggieappleton.com/notes', 1, 'section', ''),
            ('Alex Bilson', 'https://alexbilson.dev/plants', 0, 'ul.fill-list', '');
""")

if __name__ == "__main__":
    path = get_db_path()
    con = connect(path)
    create_tables(con)
    insert_defaults(con)
    con.close()
