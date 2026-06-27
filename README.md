# Asynchronous Wikipedia BFS Crawler
A high-performance, asynchronous console-based program for finding the shortest path through Wikipedia links to Adolf Hitler's biography page. 

## Overview
The program receives a link to a Wikipedia page as input. The goal is to find the shortest path to the [Adolf Hitler](https://en.wikipedia.org/wiki/Adolf_Hitler) biography page, navigating **only** through internal Wikipedia links. 
To find the shortest path through the given sites, the program uses a concurrent version of the famous **Breadth-First Search (BFS)** algorithm. 
If the program cannot find the desired path in fewer than 6 hops, it terminates its execution. To optimize the searching process, the program performs its actions asynchronously.
## Tech Stack
- **Python3** 
- **aiohttp** - asynchronous HTTP client
- **BeautifulSoup4** - HTML parsing
- **asyncio** - Concurrency
## How to Run
1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python crawler.py
   ```
## Implementation Details
Instead of a basic BFS, the program implements a network-optimized, parallelized architecture:
- **Level-Order Parallelism:** Instead of processing the queue sequentially, the algorithm groups links by their depth level and sends requests simultaneously using `asyncio.gather`.
- **Concurrency Control:** To avoid IP adress blocking by Wikipedia administrators for too many requests, this crawler uses Semaphore (`asyncio.Semaphore(100)`) to limit the amount of requests per second. This prevents the OS from crashing due to file descriptor exhaustion (`Too many open files`) as well.
- **Connection Pooling:** A single `aiohttp.ClientSession` is established at startup and passed down to the functions.
- **Cycle Prevention:** To avoid cycles in our tree of Wikipedia articles the program uses classic `set(Hash Set)` data structure. It stores the links on used articles and checks for O(1) if new link was previously added to the set.
- **Path Tracking:** The path history is preserved across parallel executions by `zip`-ping the parent node states with the awaited child results, ensuring accurate hop-by-hop tracking without race conditions.
*The time spent on the whole project is apr. 3 hours*
