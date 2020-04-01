#!/usr/bin/env python3

import glob

import markdown

CONTENT_PATH = "content/*"
SITE = {}
SITE["author"] = "Daniel Jakots"
SITE["url"] = "chown.me"


def md2html(md):
    html = markdown.markdown(md)
    return html


def get_metadata(article):
    with open(article, "r") as f:
        for line in f:
            if line.startswith("Title: "):
                title = line[7:].strip()
            elif line.startswith("Date: "):
                date = line[6:].strip()
            elif line.startswith("Category: "):
                category = line[10:].strip()
            elif line.startswith("Summary: "):
                summary = line[9:].strip()
    return title, date, category, summary


def main():
    for article in glob.glob(CONTENT_PATH):
        title, date, category, summary = get_metadata(article)
        print(title, date, category, summary, sep="\n")
        print()
    # with open("./photography.md", "r") as f:
    #     md = f.read()

    # print(md2html(md))


if __name__ == "__main__":
    main()
