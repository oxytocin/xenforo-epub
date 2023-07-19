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
        with open(TEMP_FILENAME, "a") as f:
            f.write(chapter_content + "<br/><br/>END OF POST<br/><br/>")

    for post in posts:
        process_post(post)

def extract_metadata(soup: BeautifulSoup) -> Tuple[str, str]:
    story_author_name = soup.select(".username")[0].text
    thread_title = soup.select(".p-title-value")[0].text
    return story_author_name, thread_title

def get_page_urls(base_url) -> List[str]:
    print("Enumerating pages...")
    current_page = 2
    page_urls = [base_url]  # First page is always just base url
    while True:
        page_url = f"{base_url}page-{current_page}"
        r = requests.head(page_url, allow_redirects=False)
        if r.status_code != 200:
            break
        print(f"Confirmed existence of page {current_page}")
        page_urls.append(page_url)
        current_page += 1
        time.sleep(5)
    print("Done enumerating pages")
    return page_urls

def main() -> None:
    if len(sys.argv) < 3:
        print(f"usage: {sys.argv[0]} story_url output_filename")
        sys.exit()

    with open(TEMP_FILENAME, "w") as f:
        f.write("")

    BASE_URL = sys.argv[1]
    OUT_FILENAME = sys.argv[2]
    page_urls = get_page_urls(BASE_URL)
    thread_title = story_author_name = ""
    for i, page_url in enumerate(page_urls):
        r = requests.get(page_url)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        if i == 0:
            story_author_name, thread_title = extract_metadata(soup)
        process_page(soup, story_author_name)
        print("Finished page")
        if i == len(page_urls) - 1:
            break
        time.sleep(5)
    os.system(f'pandoc --metadata title="{thread_title}" --metadata creator="{story_author_name}" {TEMP_FILENAME} -o {OUT_FILENAME}')
    os.system(f"rm {TEMP_FILENAME}")

main()
