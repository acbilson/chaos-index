import os

from bs4 import BeautifulSoup, Tag

from app.proxy import Site, File, Metadata

def parse_metadata(site: Site, page_html: str, file: File) -> Metadata:
    page = BeautifulSoup(page_html, 'html.parser')
    title = _get_title(page, site.title_query)
    content = _get_content(page, site.content_query)
    return _to_metadata(site, title, content, file)


def _get_title(page: BeautifulSoup, query: str) -> Tag:
    query_values = query.split('.')
    if len(query_values) == 2:
        tag, class_name = query_values
        return page.find(tag, class_=class_name).find_all('p')
    else:
        tag = query
        return page.find(tag)


def _get_content(page: BeautifulSoup, query: str) -> list[Tag]:
    query_values = query.split('.')
    if len(query_values) == 2:
        tag, class_name = query_values
        return page.find(tag, class_=class_name).find_all('p')
    else:
        tag = query
        return page.find(tag).find_all('p')

def _to_metadata(site: Site, title_tag: Tag, content_tags: list[Tag], file: File) -> Metadata:
    title = title_tag.getText()
    content = ''.join([x.getText() for x in content_tags])
    return Metadata(url=file.url, author=site.author, title=title, content=content, file_id=file.id)
