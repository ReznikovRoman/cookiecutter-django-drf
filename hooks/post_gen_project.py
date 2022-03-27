import os

import isort


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def append_to_project_gitignore(path: str) -> None:
    gitignore_file_path = ".gitignore"
    with open(gitignore_file_path, "a") as gitignore_file:
        gitignore_file.write(path)
        gitignore_file.write(os.linesep)


def append_to_gitignore_file(text: str) -> None:
    with open(".gitignore", "a") as gitignore_file:
        gitignore_file.write(text)
        gitignore_file.write(os.linesep)


def sort_imports_in_files(filenames: list[str]) -> None:
    for filename in filenames:
        isort.file(filename=filename)


def main() -> None:
    ignored_filenames = [
        ".env",
        "makefile.env",
        ".envs/*",
        "/*/settings/local.py",
    ]
    for ignored_filename in ignored_filenames:
        append_to_gitignore_file(ignored_filename)

    print(SUCCESS + "Project initialized!" + TERMINATOR)


if __name__ == "__main__":
    main()
