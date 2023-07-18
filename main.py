import requests
from bs4 import BeautifulSoup
import os
import time

BASE_URL = "https://forums.serebii.net/threads/losers-a-ghost-town-side-story.665637/"
TEMP_FILENAME = "temp.html"
OUT_FILENAME = "out.epub"

def process_page(page_url: str):
    # r = requests.get(page_url)
    # html = r.text

    with open("test.html") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    story_author_name = soup.select(".username")[0].text
    thread_title = soup.select(".p-title-value")[0].text
    posts = soup.select(".message-inner")

    def process_post(post):
        post_author_name = post.select(".username")[0].text
        if post_author_name != story_author_name:
            return
        chapter_content = post.select(".bbWrapper")[0].decode_contents()
        with open(TEMP_FILENAME, "a") as f:
            f.write(chapter_content + "<br/><br/>END OF POST<br/><br/>")

    os.system(f'pandoc --metadata title="{thread_title}" --metadata creator="{story_author_name}" {TEMP_FILENAME} -o {OUT_FILENAME}')

    for post in posts:
        process_post(post)

def get_page_urls(base_url):
    print("Enumerating pages...")
    current_page = 2
    page_urls = [f"{base_url}"]  # First page is always just base url
    while True:
        page_url = f"{base_url}page-{current_page}"
        r = requests.get(page_url, allow_redirects=False)
        if r.status_code != 200:
            break
        print(f"Confirmed existence of page {current_page}")
        page_urls.append(page_url)
        current_page += 1
        time.sleep(5)
    print("Done enumerating pages")
    return page_urls

def main():
    page_urls = get_page_urls(BASE_URL)
    for page_url in page_urls:
        process_page(page_url)

print(get_page_urls("https://forums.serebii.net/threads/time-and-tide.640860/"))
