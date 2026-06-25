import asyncio
import aiohttp
from collections import deque
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
TARGET = "https://en.wikipedia.org/wiki/Adolf_Hitler"
HEADERS = {
    "User-Agent": "HitlerWikiCrawler/1.0; hitlercrawler@gmail.com)"
}


async def fetch(url: str, session: aiohttp.ClientSession) ->str:
    async with session.get(url) as response:
        return await response.text()


async def extract_links(url: str, session: aiohttp.ClientSession) -> list:
    html_text = await fetch(url, session)

    soup = BeautifulSoup(html_text, 'html.parser')
    
    valid_urls = []
    for link in soup.find_all('a'):
        prop_link = link.get('href')
        if is_valid_wiki_link(prop_link):
            valid_urls.append(urljoin(BASE_URL, prop_link))

    return valid_urls



def is_valid_wiki_link(href: str) -> bool:
    if not href:
        return False

    if not href.startswith("/wiki/"):
        return False

    if ":" in href:
        return False

    return True


async def bfs(start_url: str, max_moves: int = 6) -> list:
    used = set([start_url])
    queue = deque([(start_url, 0, [start_url])])

    async with aiohttp.ClientSession(headers= HEADERS) as session:
        while queue:
            current_url, moves, path = queue.popleft()

            if current_url == TARGET:
                return path

            if moves > max_moves:
                continue

            moves += 1
            urls = await extract_links(current_url, session)

            for url in urls:
                if url not in used:
                    used.add(url)
                    queue.append((url, moves, path + [url]))
    
    return None


async def main():
    initial_link = input("Input the wikipedia link: ")
    print(f"Starting search with the {initial_link}")
    path = await bfs(initial_link)

    if path:
        print("Path exists! You have to go through: ")
        print(" ->\n".join(path))

    else:
        print("Path does not exist within 6 moves")


if __name__ == "__main__":
    asyncio.run(main())