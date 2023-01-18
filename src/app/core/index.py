import os
import json
import argparse
from urllib.parse import urljoin, urlparse
from collections import namedtuple


def save_index(data: list[Metadata]) -> None:
    content = []
    for metadata in metadatas:
        content.append(dict(id=metadata.url, author=metadata.author, title=metadata.title, content=metadata.content))
    return json.dumps(content)
