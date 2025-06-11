import os
import fnmatch
from pathlib import Path


def read_gitignore():
    gitignore_path = "./.gitignore"
    if not os.path.exists(gitignore_path):
        return []

    with open(gitignore_path, "r") as file:
        lines = file.readlines()

    patterns = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return [*patterns, ".git"]


def is_ignored(path: str, gitignore_patterns: list) -> bool:
    path_obj = Path(path)
    for pattern in gitignore_patterns:
        if pattern.endswith("/"):
            dir_pattern = pattern.rstrip("/")
            if fnmatch.fnmatch(path_obj.name, dir_pattern) and path_obj.is_dir():
                return True
        if fnmatch.fnmatch(path_obj.name, pattern):
            return True
    return False


def list_all_files(dir_path, gitignore_patterns, base_dir=None):
    if base_dir is None:
        base_dir = dir_path

    files = []
    try:
        with os.scandir(dir_path) as entries:
            for entry in entries:
                entry_path = os.path.normpath(entry.path)
                relative_path = os.path.relpath(entry_path, start=base_dir)

                if is_ignored(entry.name, gitignore_patterns) or is_ignored(
                    relative_path, gitignore_patterns
                ):
                    continue

                if entry.is_file(follow_symlinks=False):
                    files.append(entry_path)
                elif entry.is_dir(follow_symlinks=False):
                    files.extend(list_all_files(entry_path, gitignore_patterns, base_dir))
    except PermissionError:
        pass

    return files


def read_path_caption(paths: list[str]) -> str:
    res: list[str] = []

    for p in paths:
        try:
            with open(p, "r") as file:
                res.append(file.read())
            res.append(p)
        except Exception:
            continue
    cock = []
    for line in res:
        if line.strip() == "\n":
            continue
        cock.append(line)

    return "\n".join(cock)


def main():
    gitignore_patterns = read_gitignore()
    path = os.path.normpath(".")
    paths = list_all_files(path, gitignore_patterns)
    res = read_path_caption(paths)
    print(res)


if __name__ == "__main__":
    main()
