import streamlit as st
import pandas as pd

from backend.booli_route.booli_api import Query
from frontend import api_caller
from frontend.additional_filters import additional_filters

st.set_page_config("House Search", page_icon="🏠", layout="wide")

buildings = ["alla", "villa", "lägenhet", "gård", "tomt-mark", "fritidshus", "parhus", "radhus", "kedjehus"]
buildings_en = ["All Types", "🏠 House", "Apartment", "Farm", "Land Area", "Cottage", "Semi-Detached House", "Townhouse",
                "Terraced House"]
buildings = {en: se for se, en in zip(buildings, buildings_en)}


def main():
    st.title("House Search by Us")
    with st.form(key="filter-form"):
        query = st.text_input("Where", placeholder="Where do you want to live?",
                              help="Can be a free-text, coordinate or other.")
        buffer = st.slider("Expand Area with", 0, 300, 0, 10, format="%d km")

        building_types = st.multiselect("Building Type", buildings_en, default=["All Types"])
        building_types = [buildings[building_type] for building_type in building_types]
        if "alla" in building_types:
            building_types = None

        filter_data = additional_filters()

        submitted = st.form_submit_button("Find Houses!")
    if submitted:
        props = filter_data.house_properties
        query = Query(query=query, dim=str(buffer * 1000), price_interval=props.price,
                      rooms=props.rooms, living_area=props.area,
                      object_type=building_types, is_new_construction=props.new_production)

        # houses = api_caller.get_booli_listings(query.json())
        houses = api_caller.get_booli_listings(query, query.json())

        c1, c2 = st.columns([3, 1])
        with c1:
            for house in houses:
                st.subheader(house.location.address.streetAddress)
                st.dataframe(pd.DataFrame([house.dict()]).T, use_container_width=True)

                pass
        with c2:
            st.markdown(
                "<div style='background:lightgray;padding:10px;border-radius:6px;height: 250px;'>Kul att veta :)</div>",
                unsafe_allow_html=True)


if __name__ == '__main__':
    main()
