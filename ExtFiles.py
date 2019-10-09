from os import path


def get(name):
    base_path = path.dirname(path.abspath(__file__))
    return path.join(base_path, name)
