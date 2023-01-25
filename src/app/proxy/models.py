class Site:
    def __init__(
        self,
        author: str,
        url: str,
        partial_links: int,
        link_query: str,
        title_query: str,
        content_query: str,
        rowid=None,
    ):
        self.id = int(rowid) if rowid is not None else None
        self.author = author
        self.url = url
        self.partial_links = partial_links == 1
        self.link_query = link_query
        self.title_query = title_query
        self.content_query = content_query

    def __str__(self):
        return f"Site <{self.url}>"

    def __repr__(self):
        return self.__str__()


class File:
    def __init__(self, url: str, path: str, site_id: str, rowid=None):
        self.id = int(rowid) if rowid is not None else None
        self.url = url
        self.path = path
        self.site_id = int(site_id)

    def __str__(self):
        return f"File <{self.url}>"

    def __repr__(self):
        return self.__str__()


class Metadata:
    def __init__(
        self,
        url: str,
        author: str,
        title: str,
        content: str,
        file_id: int,
        site_id: int,
    ):
        self.url = url
        self.author = author
        self.title = title
        self.content = content
        self.file_id = file_id
        self.site_id = site_id

    def __str__(self):
        return f"Metadata <{self.url}>"

    def __repr__(self):
        return self.__str__()
