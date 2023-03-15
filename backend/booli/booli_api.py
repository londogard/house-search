from dataclasses import dataclass
import requests

# https://www.booli.se/p/api/referens
CORE_URL = "https://api.booli.se/"
LISTINGS_URL = f"{CORE_URL}listings"

@dataclass
class Query:
    query: str | None = None
    center_coordinate: tuple[float, float] | None = None
    # https://www.booli.se/p/api/referens

def get_listing(_id: str):
    r = requests.get(f"{LISTINGS_URL}/{_id}")
    r.raise_for_status()
    
    return r.json()

def get_listings(query: Query):
    r = requests.get(f"{LISTINGS_URL}?{id}")
    r.raise_for_status()
    
    return r.json()