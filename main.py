import requests
from bs4 import BeautifulSoup

URL = "https://forums.serebii.net/threads/losers-a-ghost-town-side-story.665637/"

# r = requests.get(URL)
# html = r.text

with open("test.html") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
story_author_name = soup.select(".username")[0].text
posts = soup.select(".message-inner")

def process_post(post):
    post_author_name = post.select(".username")[0].text
    if post_author_name != story_author_name:
        return
    chapter_content = post.select(".bbWrapper")[0].decode_contents()
    with open("temp.html", "a") as f:
        f.write(chapter_content + "<br/><br/>END OF POST<br/><br/>")

for post in posts:
    process_post(post)
