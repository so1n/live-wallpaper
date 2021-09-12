from os import path


def get_file_path(file: str) -> str:
    return path.abspath(path.dirname(file))
