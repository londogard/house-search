import streamlit as st
import pandas as pd


from backend.booli_route.booli_api import Query
from frontend import api_caller

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

        with st.expander("Additional Filters"):
            c1, c2, c3 = st.columns(3)
            with c1:
                rooms = st.slider("No of Rooms", 0, 15, (0, 15))
                new_production = st.checkbox("Is New Construction")
            with c2:
                area = st.slider("Living Area", 0, 250, (0, 250), 10, format="%d m²")
            with c3:
                price = st.slider("Price (milion SEK)", 0., 20., (0., 20.), 0.1, format="%.1f")

        submitted = st.form_submit_button("Find Houses!")
    if submitted:
        query = Query(query=query, dim=str(buffer * 1000), price_interval=price, rooms=rooms, living_area=area,
                  object_type=building_types, is_new_construction=new_production)
        houses = api_caller.get_booli_listings(query.json())

        for house in houses:
            st.subheader(house.location.address.streetAddress)
            st.dataframe(pd.DataFrame([house.dict()]).T)
            # st.write(house)
            pass



if __name__ == '__main__':
    main()
