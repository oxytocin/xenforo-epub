#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import os
import time
from typing import *
import sys

TEMP_FILENAME = "temp.html"

def process_page(soup: BeautifulSoup, story_author_name: str) -> None:
    posts = soup.select(".message-inner")

    def process_post(post):
        post_author_name = post.select(".username")[0].text
        if post_author_name != story_author_name:
            return
        chapter_content = post.select(".bbWrapper")[0].decode_contents()
        chapter_content = f"<p>{chapter_content}</p>"
        chapter_content = chapter_content.replace("\n", "</p><p>")
        chapter_content = chapter_content.replace("<br/>", "")
        with open(TEMP_FILENAME, "a") as f:
            f.write(chapter_content + "<br/><br/>END OF POST<br/><br/>")

    for post in posts:
        process_post(post)

def extract_metadata(soup: BeautifulSoup) -> Tuple[str, str]:
    story_author_name = soup.select(".username")[0].text
    thread_title = soup.select(".p-title-value")[0].text
    return story_author_name, thread_title

def main() -> None:
    if len(sys.argv) < 3:
        print(f"usage: {sys.argv[0]} story_url output_filename")
        sys.exit()

    with open(TEMP_FILENAME, "w") as f:
        f.write("")

    BASE_URL = sys.argv[1]
    OUT_FILENAME = sys.argv[2]
    thread_title = story_author_name = ""
    pageno = 1
    while True:
        url = BASE_URL if pageno == 1 else f"{BASE_URL}page-{pageno}"
        r = requests.get(url, allow_redirects=False)
        if r.status_code != 200:
            break
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        if pageno == 1:
            story_author_name, thread_title = extract_metadata(soup)
        process_page(soup, story_author_name)
        print(f"Finished page {pageno}")
        time.sleep(5)
        pageno += 1

    os.system(f'pandoc --metadata title="{thread_title}" --metadata creator="{story_author_name}" {TEMP_FILENAME} -o {OUT_FILENAME}')
    os.system(f"rm {TEMP_FILENAME}")

main()
