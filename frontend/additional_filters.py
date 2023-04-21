import streamlit as st
from pydantic import BaseModel


class HouseProperties(BaseModel):
    rooms: tuple[int, int]
    new_production: bool
    area: tuple[int, int]
    price: tuple[float, float]


def house_property_filter() -> HouseProperties:
    c1, c2, c3 = st.columns(3)
    with c1:
        rooms = st.slider("No of Rooms", 0, 15, (0, 15))
        new_production = st.checkbox("Is New Construction")
    with c2:
        area = st.slider("Living Area", 0, 250, (0, 250), 10, format="%d m²")
    with c3:
        price = st.slider(
            "Price (milion SEK)", 0.0, 20.0, (0.0, 20.0), 0.1, format="%.1f"
        )
        price = [p * 1e6 for p in price]

    return HouseProperties(
        rooms=rooms, new_production=new_production, area=area, price=price
    )


class NearbyFilter(BaseModel):
    distance: float
    bus_stop: bool
    gym: bool
    convenience_store: bool
    restaurants: bool
    bathing_place: bool


def nearby_filter():
    default = st.slider("Max Distance", 0.0, 50.0, 5.0, 0.5, format="%.1f km")
    bus_stop = st.checkbox("Bus Stops")
    gym = st.checkbox("Gym")
    convenience_store = st.checkbox("Convenience Store")
    restaurants = st.checkbox("Restaurants")
    bathing_place = st.checkbox("Bathing Place")

    return NearbyFilter(
        distance=default,
        bus_stop=bus_stop,
        gym=gym,
        convenience_store=convenience_store,
        restaurants=restaurants,
        bathing_place=bathing_place,
    )


class FilterData(BaseModel):
    house_properties: HouseProperties
    nearby: NearbyFilter


def additional_filters() -> FilterData:
    with st.expander("Additional Filters"):
        t1, t2 = st.tabs(["House Properties", "Nearby"])
        with t1:
            house_filter_data = house_property_filter()
        with t2:
            nearby_filter_data = nearby_filter()

    return FilterData(house_properties=house_filter_data, nearby=nearby_filter_data)
