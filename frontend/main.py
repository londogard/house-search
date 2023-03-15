import streamlit as st
import pandas as pd

from backend.booli_route.booli_api import Query
from frontend import api_caller
from frontend.additional_filters import additional_filters
import osm_query
from typing import Any
from osm_query import get_pois_in_range_by_filter

@st.cache_resource
def get_tags() -> dict[str, Any]:
    return osm_query.get_tag_dict()


st.set_page_config("Home Finder", page_icon="🏠", layout="wide")

buildings = ["alla", "villa", "lägenhet", "gård", "tomt-mark", "fritidshus", "parhus", "radhus", "kedjehus"]
buildings_en = ["All Types", "🏠 House", "Apartment", "Farm", "Land Area", "Cottage", "Semi-Detached House", "Townhouse",
                "Terraced House"]
buildings = {en: se for se, en in zip(buildings, buildings_en)}


def main():
    st.title("Home Finder 🔍 (by HEMA)")
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
        if not len(query):
            return st.warning("Query is empty, please add something!!")

        props = filter_data.house_properties

        query = Query(query=query, dim=str(buffer * 1000), price_interval=props.price,
                      rooms=props.rooms, living_area=props.area,
                      object_type=building_types, is_new_construction=props.new_production)

        # houses = api_caller.get_booli_listings(query.json())
        houses = api_caller.get_booli_listings(query, query.json())
        c1, c2 = st.columns([3, 1])
        with c1:
            missing_houses = []
            for house in houses:
                coord = (house.location.position.latitude, house.location.position.longitude)
                gdf, passing = get_pois_in_range_by_filter(filter_data.nearby, coord, filter_data.nearby.distance * 1000)

                if passing:
                    rent = "." if house.rent is None else f" with {house.rent} SEK/month rent."

                    st.subheader(f"{house.location.address.streetAddress} ({house.location.address.city})")

                    rows = [
                        f"**{house.objectType}** with {house.rooms} rooms ({house.livingArea} m²).  \n"
                        f"Listing Price is {house.listPrice / 1e6} million SEK{rent}  \n",
                        f"[booli.se]({house.url})"
                    ]
                    st.markdown("".join(rows), unsafe_allow_html=True)
                    if gdf is not None:
                        with st.expander("Show nearby"):
                            st.dataframe(gdf.drop(["geometry", "osmid", "nodes", "element_type"], axis="columns", errors="ignore"), use_container_width=True)
                    st.write("---")
                else:
                    missing_houses.append(house.location.address.streetAddress)

            if len(missing_houses):
                st.subheader("Houses not fulfilling the criterias")
                st.write(", ".join(missing_houses))

            st.subheader("Quick Compare All")
            df = pd.DataFrame([h.dict() for h in houses])
            df = df.drop(["source", "booliId", "location"], axis="columns", errors="ignore")
            st.dataframe(df, use_container_width=True)
        with c2:
            st.markdown(
                "<div style='background:lightgray;padding:10px;border-radius:6px;height: 250px;'>Kul att veta :)</div>",
                unsafe_allow_html=True)


if __name__ == '__main__':
    main()
