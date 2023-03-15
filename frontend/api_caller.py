import streamlit as st

from backend.booli_route import booli
from backend.booli_route.booli_api import PropertyResponse, Query
import json

BASE_URL = "http://localhost:8000"


@st.cache_data()
def get_booli_listings(_query: Query, key: str):
    return booli.get_listings(_query)
    #r = requests.post(f"{BASE_URL}/booli_route/query", data=query_json)
    #r.raise_for_status()
    #
    #return [PropertyResponse(**x) for x in r.json()]
