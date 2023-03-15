import requests
import streamlit as st

from backend.booli_route.booli_api import PropertyResponse, Query
import json

BASE_URL = "http://localhost:8000"


@st.cache_data
def get_booli_listings(query_json: str):
    r = requests.post(f"{BASE_URL}/booli_route/query", data=query_json)
    r.raise_for_status()

    return [PropertyResponse(**x) for x in r.json()]
