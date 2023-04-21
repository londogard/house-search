import requests
from bs4 import BeautifulSoup
import re


def extract_max_page(pages: list[str]) -> int:
    []


def scrape_listing_url(url: str):
    # Visar 1 - 50 av 2500... = indexing
    user_agent = {"User-agent": "Mozilla/5.0"}
    request = requests.get(url, headers=user_agent, timeout=30)
    request.raise_for_status()
    html_doc = request.text

    soup = BeautifulSoup(html_doc, "html.parser")
    refs = soup.find_all(href=re.compile(r"/bostader.*?page=\d+"))
    max_page = max([int(r.string) for r in refs if r.string.isdigit()])
    range(max_page)

    print(max_page)
    print(refs)
    pass


if __name__ == "__main__":
    url = "https://www.hemnet.se/bostader?location_ids=17753&item_types=villa&page="
    scrape_listing_url(url)
