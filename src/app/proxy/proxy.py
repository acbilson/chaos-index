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
        cur = self.con.cursor()
        in_db = (
            cur.execute("SELECT * FROM file WHERE url == ?", [file.url]).fetchone()
            is not None
        )
        cur.close()
        return in_db

    def read_sites(self) -> list[Site]:
        cur = self.con.cursor()
        sites = []
        for x in cur.execute(
            "SELECT rowid, author, url, partial_links, link_query, title_query, content_query FROM site;"
        ):
            sites.append(
                Site(
                    rowid=x[0],
                    author=x[1],
                    url=x[2],
                    partial_links=x[3],
                    link_query=x[4],
                    title_query=x[5],
                    content_query=x[6],
                )
            )
        cur.close()
        return sites

    def create_files(self, files: list[File]) -> None:
        cur = self.con.cursor()
        data = [(x.url, x.path, x.site_id) for x in files]
        cur.executemany("INSERT INTO file VALUES (?, ?, ?, CURRENT_DATE)", data)
        self.con.commit()
        cur.close()

    def read_files_without_metadata(self) -> list[File]:
        cur = self.con.cursor()
        files = []
        for x in cur.execute(
            """
            SELECT f.rowid, f.url, f.path, f.site_id
            FROM file f
            LEFT JOIN metadata m
                ON m.file_id = f.rowid
            WHERE m.file_id IS NULL;
        """):
            files.append(File(rowid=x[0], url=x[1], path=x[2], site_id=x[3]))
        cur.close()
        return files

    def create_metadatas(self, site_id: int, metadatas: list[Metadata]) -> None:
        cur = self.con.cursor()
        cur.executemany("INSERT INTO metadata VALUES (?, ?)", [(site_id, x.file_id) for x in metadatas])
        cur.executemany("INSERT INTO metadata_fts VALUES (?, ?, ?)", [(x.file_id, x.title, x.content) for x in metadatas])
        self.con.commit()
        cur.close()

    def query_metadata(self, query: str) -> tuple[list[Metadata], str]:
        msg = ""
        cur = self.con.cursor()
        metadata = []
        try:
            for x in cur.execute(
                """
                SELECT f.url,
                       author,
                       title,
                       snippet(metadata_fts, 2, '<span class="highlight">', '</span>', '', 30),
                       m.file_id,
                       s.rowid
                FROM metadata_fts m
                join file f on m.file_id = f.rowid
                join site s on f.site_id = s.rowid
                where content match ?;
                """,
                [query],
            ):
                if len(x) > 4:
                    metadata.append(
                        Metadata(
                            url=x[0],
                            author=x[1],
                            title=x[2],
                            content=x[3],
                            file_id=x[4],
                            site_id=x[5],
                        )
                    )
        except sqlite3.OperationalError as e:
            msg = "".join(e.args)

        cur.close()
        return metadata, msg

    def read_sites_with_page_count(self) -> tuple[list[dict], str]:
        msg = ""
        cur = self.con.cursor()
        results = []
        try:
            for x in cur.execute(
                """
                SELECT s.author, s.url, count(f.rowid) as 'pages'
                FROM site s LEFT JOIN file f
                    ON f.site_id = s.rowid
                GROUP BY s.author, s.url;
            """
            ):
                results.append(dict(author=x[0], url=x[1], pages=x[2]))

        except sqlite3.OperationalError as e:
            msg = "".join(e.args)

        cur.close()
        return results, msg
