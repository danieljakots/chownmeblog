#!/usr/bin/env python3

import glob
import sys

import markdown

CONTENT_PATH = "content/*"
SITE = {}
SITE["author"] = "Daniel Jakots"
SITE["url"] = "chown.me"


def md2html(md):
    html = markdown.markdown(md)
    return html


def parse_article(article_path):
    article = {}
    with open(article_path, "r") as f:
        metadata = [next(f) for x in range(4)]
        for line in metadata:
            if line.startswith("Title: "):
                article["title"] = line[7:].strip()
            elif line.startswith("Date: "):
                article["date"] = line[6:].strip()
            elif line.startswith("Category: "):
                article["category"] = line[10:].strip()
            elif line.startswith("Summary: "):
                article["summary"] = line[9:].strip()
        article["markdown"] = f.read()

    if len(article) < 5:
        print(f"There's a problem with metadata for {article_path}")
        sys.exit(1)
    return article


def parse_articles(content_path):
    content = []
    for article in glob.glob(content_path):
        article = parse_article(article)
        content.append(article)
    return content


def main():
    content = parse_articles(CONTENT_PATH)
    # with open("./photography.md", "r") as f:
    #     md = f.read()

    # print(md2html(md))


if __name__ == "__main__":
    main()
