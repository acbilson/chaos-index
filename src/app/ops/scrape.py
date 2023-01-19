import os
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup, Tag
import requests

from app.proxy import Site, File


def scrape_site(site: Site, root_dir: str) -> list[File]:
    page = _get_page(site.url)
    link_tags = _query_link_tags(page, site.link_query)
    urls = _get_urls(link_tags, site.partial_links, site.url)
    return _urls_to_files(site, urls, root_dir)


def scrape_page(url: str) -> str:
    resp = requests.get(url)
    return resp.text if resp.status_code == 200 else None


def _get_page(url: str) -> BeautifulSoup:
    resp = requests.get(url)
    return BeautifulSoup(resp.content, 'html.parser') if resp.status_code == 200 else None


def _query_link_tags(page: BeautifulSoup, query: str) -> list[Tag]:
    query_values = query.split('.')
    if len(query_values) == 2:
        tag, class_name = query_values
        return page.find(tag, class_=class_name).find_all('a')
    else:
        tag = query
        return page.find(tag).find_all('a')


def _get_urls(tags: list[Tag], partial_links: bool, root_url: str) -> list[str]:
    if partial_links:
        return [urljoin(root_url, x.get('href')) for x in tags]
    else:
        return [x.get('href') for x in tags]


def _urls_to_files(site: Site, urls: list[str], root_dir: str) -> list[File]:
    files = []
    for url in urls:
        path = _get_full_path(site.author, root_dir, url)
        files.append(File(url=url, path=path, site_id=site.id))
    return files


def _get_full_path(author: str, root_dir: str, url: str) -> str:
    root = os.path.join(root_dir, author.lower().replace(' ', '-'))
    stem = urlparse(url).path.strip('/').replace('/', '_')
    return os.path.join(root_dir, root, stem + '.html')
