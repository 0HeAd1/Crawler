import asyncio
import aiohttp
from collections import deque
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
TARGET = "https://en.wikipedia.org/wiki/Adolf_Hitler"
HEADERS = {
    "User-Agent": "HitlerWikiCrawler/1.0 (hitlercrawler@gmail.com)"
}


async def fetch(url: str, session: aiohttp.ClientSession, sem: asyncio.Semaphore) ->str:
    async with sem:
        async with session.get(url) as response:
            return await response.text()


async def extract_links(url: str, session: aiohttp.ClientSession, sem: asyncio.Semaphore) -> list:
    html_text = await fetch(url, session, sem)

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


async def bfs(start_url: str, session: aiohttp.ClientSession, max_moves: int = 6) -> list:
    if start_url == TARGET:
        return [start_url]
    
    used = set([start_url])
    current_lvl = [(start_url, [start_url])]

    sem = asyncio.Semaphore(100)
    for move in range(max_moves):
        tasks = []

        for node in current_lvl:
            task = extract_links(node[0], session, sem)
            tasks.append(task)
            
        results = await asyncio.gather(*tasks)

        next_lvl = []

        for parent, child_urls in zip(current_lvl, results):
            parent_url, parent_path = parent

            for child in child_urls:
                if child == TARGET:
                    return parent_path + [child]
                    
                if child not in used:
                    used.add(child)
                    next_lvl.append((child, parent_path + [child]))
            
        current_lvl = next_lvl

    return None


async def main():
    print("Input the word 'exit' to leave the program.")
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while True:
            initial_link = input("Input the wikipedia link: ")

            if initial_link.lower() == 'exit':
                print("Goodbye!")
                break
            if not initial_link:
                continue
            

            print(f"Starting search with the {initial_link}")
            path = await bfs(initial_link, session)

            if path:
                print("Path exists! You have to go through: ")
                print(" ->\n".join(path))

            else:
                print("Hitler not found")


if __name__ == "__main__":
    asyncio.run(main())