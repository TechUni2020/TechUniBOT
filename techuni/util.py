import os

def multi_dirname(path: str, n: int) -> str:
    path = os.path.abspath(path)
    for _ in range(n):
        path = os.path.dirname(path)
    return path
