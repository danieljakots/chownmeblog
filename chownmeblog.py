#!/usr/bin/env python3

import glob
import sys

import jinja2
import markdown

CONTENT_PATH = "content/*"
SITE = {}
SITE["author"] = "Daniel Jakots"
SITE["url"] = "https://oldblog.chown.me"
OUTPUT_DIR = "output"


def md2html(md):
    html = markdown.markdown(md)
    return html


def parse_article(article_path):
    article = {}
    article[
        "file"
    ] = f"blog/{article_path.replace('.md', '.html')[len(CONTENT_PATH) - 1:]}"
    with open(article_path, "r") as f:
        metadata = [next(f) for x in range(3)]
        for line in metadata:
            if line.startswith("Title: "):
                article["title"] = line[7:].strip()
            elif line.startswith("Date: "):
                article["date"] = line[6:].strip()
            elif line.startswith("Category: "):
                article["category"] = line[10:].strip()
        article["markdown"] = f.read()

    if len(article) < 4:
        print(f"There's a problem with metadata for {article_path}")
        sys.exit(1)
    return article


def parse_articles(content_path):
    content = []
    for article in glob.glob(content_path):
        article = parse_article(article)
        content.append(article)
    content.sort(reverse=True, key=lambda i: i["date"])
    return content


def generate_website(content):
    jinja2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"), trim_blocks=True
    )
    jinja2_template = jinja2_env.get_template("index.html.j2")
    result = jinja2_template.render(articles=content, site=SITE)
    with open(f"{OUTPUT_DIR}/index.html", "w") as f:
        f.write(result)

    jinja2_template = jinja2_env.get_template("article.html.j2")
    for article in content:
        result = jinja2_template.render(article=article, site=SITE)
        with open(f"{OUTPUT_DIR}/{article['file']}", "w") as f:
            f.write(result)


def main():
    content = parse_articles(CONTENT_PATH)
    for article in content:
        article["html"] = md2html(article.pop("markdown"))
    generate_website(content)


if __name__ == "__main__":
    main()
