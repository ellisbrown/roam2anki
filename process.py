import os
import re
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


replacements: List[Tuple[str, str]] = [
    (r"\#(\[\[.+\]\])", r"\1"),  # '#[[...]]' -> '[[..]]'
    (r"\[\[(.+)\]\]", r"\1"),  # '[[..]]' -> '..'
    (r"\#(\w*)\b", r"\1"),  # '#...' -> '...'
    (r"\*\*(.*)\*\*", r"<b>\1</b>"),  # md bold to html bold
    (r"\$\$(.*?)\$\$", r"\(\1\)"),  # '$$...$$' -> '\(...\)'
]


def replace(string: str, replacements: List[Tuple[str, str]] = replacements):
    for x, y in replacements:
        string = re.sub(x, y, string)
    return string


def process(path: str) -> None:
    with open(path, "r") as file:
        contents: str = file.read()

    processed = replace(contents)
    return processed


def main():
    inbox = os.listdir("inbox")
    for f in inbox:
        if f[-3:] != ".md":
            logger.info(f"skipped {f} - not markdown")

        infile = os.path.join("inbox", f)
        outfile = os.path.join("processed", f)

        # process
        processed = process(infile)

        # move
        os.rename(infile, outfile)

        # overwrite
        with open(outfile, "w") as file:
            file.write(processed)


if __name__ == "__main__":
    main()
