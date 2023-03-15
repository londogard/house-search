import json

from backend.booli_route.booli_api import PropertyResponse, Query, LISTINGS_URL, QueryResponse
from fastapi import APIRouter
import requests

router = APIRouter(prefix="/booli_route")


@router.get("/listing/{_id}")
def get_listing(_id: str) -> PropertyResponse:
    r = requests.get(f"{LISTINGS_URL}/{_id}")
    r.raise_for_status()
    response = r.json()
    response = PropertyResponse(**response["listings"][0])
    # TODO wrap and get all listings rather than first [limit]

    return response


@router.post("/query")
def get_listings(query: Query) -> list[PropertyResponse]:
    print(f"{LISTINGS_URL}?{query.build_params()}")
    r = requests.get(f"{LISTINGS_URL}?{query.build_params()}")
    r.raise_for_status()
    r_json = r.json()["body"]

    if len(r_json):
        # TODO wrap and get all listings rather than first [limit]
        try:
            response = QueryResponse(**json.loads(r_json))
        except TypeError as e:
            return []

        return response.listings
    else:
        raise Exception("No listings found")

if __name__ == "__main__":
    print(get_listings(Query(query="malmö")))