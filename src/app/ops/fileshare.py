import os


def create_root_dir(root_dir: str, author: str) -> None:
    path = os.path.join(root_dir, author.lower().replace(" ", "-"))
    if not os.path.exists(path):
        os.makedirs(path)


def write_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def read_file(path: str) -> str:
    content = []
    with open(path, "r") as f:
        content = f.read()
    return content
