import sqlite3
from bs4 import Tag

from .models import Site, File, Metadata

class SqlProxy:

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.con = None


    def connect(self) -> None:
        self.con = sqlite3.connect(self.db_path)


    def disconnect(self):
        self.con.close()


    def file_in_db(self, file: File) -> bool:
        return self.con.cursor().execute(f"SELECT * FROM file WHERE url == '{file.link}'").fetchone is not None


    def read_sites(self) -> list[Site]:
        sites = []
        for x in self.con.cursor().execute("SELECT rowid, author, url, partial_links, link_query, title_query, content_query FROM site;"):
            sites.append(Site(rowid=x[0], author=x[1], url=x[2], partial_links=x[3], link_query=x[4], title_query=x[5], content_query=x[6]))
        return sites


    def create_files(self, files: list[File]) -> None:
        data = [(x.link, get_full_path(x), x.site_id) for x in files]
        self.con.cursor().executemany("INSERT INTO file VALUES (?, ?, ?, CURRENT_DATE)", data)
        self.con.commit()


    def read_files_without_metadata(self, site_id: int) -> list[File]:
        files = []
        for x in self.con.cursor().execute("""
            SELECT f.rowid, f.url, f.path, f.site_id
            FROM file f
            LEFT JOIN metadata m
                ON m.file_id = f.rowid
            WHERE m.rowid is NULL
                AND f.site_id = ?;
        """, (str(site_id))):
            files.append(File(rowid=x[0], url=x[1], path=x[2], site_id=x[3]))
        return files


    def create_metadatas(self, metadatas: list[Metadata]) -> None:
        data = [(x.title, x.content, x.file_id) for x in metadatas]
        self.con.cursor().executemany("INSERT INTO metadata VALUES (?, ?, ?)", data)
        self.con.commit()


    def read_metadatas(self) -> list[Metadata]:
        metadata = []
        for x in self.con.cursor().execute("""
            SELECT m.rowid, f.url, author, title, content, file_id
            FROM metadata m
            join file f on m.file_id = f.rowid
            join site s on f.site_id = s.rowid;
            """):
            metadata.append(Metadata(rowid=x[0], url=x[1], author=x[2], title=x[3], content=x[4], file_id=x[5]))
        return metadata

