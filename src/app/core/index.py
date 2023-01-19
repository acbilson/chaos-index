import os
import argparse
from urllib.parse import urljoin, urlparse
from collections import namedtuple

from app.core.models import Metadata


def save_index(metadatas: list[Metadata]) -> list[dict]:
    content = []
    for metadata in metadatas:
        content.append(dict(id=metadata.url, author=metadata.author, title=metadata.title, content=metadata.content))
    return content
