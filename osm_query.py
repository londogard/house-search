import os
from typing import Any

import osmnx as ox
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Polygon

from frontend.additional_filters import NearbyFilter

os.environ["USE_PYGEOS"] = "0"


ox.config(log_console=True, use_cache=True)


def get_tag_dict() -> dict[str, Any]:
    feats = ["bus_stop", "convenience_store", "restaurant", "gym", "water"]
    tags = [
        {
            "public_transport": ["stop_position", "platform", "station", "stop_area"],
            "railway": [
                "rail",
                "subway",
                "tram",
                "light_rail",
                "monorail",
                "monorail_service",
            ],
            "amenity": ["bus_station", "bicycle_rental"],
        },
        {
            "shop": ["convenience", "frozen_food", "greengrocer", "supermarket"],
        },
        {
            "amenity": [
                "restaurant",
                "cafe",
                "fast_food",
                "food_court",
                "biergarten",
                "pub",
            ],
        },
        {
            "leisure": [
                "fitness_centre",
                "fitness_station",
                "sports_hall",
                "sports_centre",
            ],
            "sport": ["fitness"],
            "building": ["sports_hall"],
        },
        {
            "natural": ["beach"],
            "leisure": ["bathing_place"],
        },
    ]
    return dict(zip(feats, tags))


def get_pois_in_range_by_filter_efficient(
    nearby: NearbyFilter, center: tuple[float, float], buffer_meters: int | None
) -> GeoDataFrame:
    tags = get_tag_dict()
    selected_tags = []
    selected_tag_dict = {}
    if nearby.bathing_place:
        selected_tags.append(tags["water"])
    if nearby.gym:
        selected_tags.append(tags["gym"])
    if nearby.bus_stop:
        selected_tags.append(tags["bus_stop"])
    if nearby.restaurants:
        selected_tags.append(tags["restaurant"])
    if nearby.convenience_store:
        selected_tags.append(tags["convenience_store"])

    for tag in selected_tags:
        for k, v in tag.items():
            selected_tag_dict[k] = v + selected_tag_dict.get(k, [])

    return get_pois_in_range(center, buffer_meters, selected_tag_dict)


def get_pois_in_range_by_filter(
    nearby: NearbyFilter, center: tuple[float, float], buffer_meters: int | None
) -> tuple[GeoDataFrame | None, bool]:
    passing = True
    gdfs = []
    if nearby.bathing_place:
        water = get_water_in_range(center, buffer_meters)
        passing = passing and not water.empty
        gdfs.append(water)
    if nearby.gym:
        gym = get_gyms_in_range(center, buffer_meters)
        passing = passing and not gym.empty
        gdfs.append(gym)
    if nearby.restaurants:
        restaurants = get_restaurants_in_range(center, buffer_meters)
        passing = passing and not restaurants.empty
        gdfs.append(restaurants)
    if nearby.bus_stop:
        bus_stops = get_bus_stops_in_range(center, buffer_meters)
        passing = passing and not bus_stops.empty
        gdfs.append(bus_stops)
    if nearby.convenience_store:
        convenience_stores = get_convenience_stores_in_range(center, buffer_meters)
        passing = passing and not convenience_stores.empty
        gdfs.append(convenience_stores)

    if len(gdfs):
        gdf = pd.concat(gdfs)
        gdf["size"] = 1
        return (gdf, passing)

    return (None, passing)


def get_pois_in_range(
    center: tuple[float, float] | Polygon | str,
    buffer_meters: int | None,
    tags: dict[str, Any],
) -> GeoDataFrame:
    match center:
        # additionally exists like _from_address, _from_place, ...
        case tuple():
            return ox.geometries_from_point(center, dist=buffer_meters, tags=tags)
        case Polygon():
            return ox.geometries_from_polygon(center, tags=tags)
        case str():
            return ox.geometries_from_place(center, tags=tags)


def get_bus_stops_in_range(
    center: tuple[float, float] | Polygon | str, buffer_meters: int | None
) -> GeoDataFrame:
    tags = {
        "public_transport": ["stop_position", "platform", "station", "stop_area"],
        # "railway": ["rail", "subway", "tram", "light_rail", "monorail", "monorail_service"],
        "amenity": ["bus_station", "bicycle_rental"],
    }
    gdf = get_pois_in_range(center, buffer_meters, tags)
    gdf["type"] = "bus_stop"
    return gdf


def get_convenience_stores_in_range(
    center: tuple[float, float] | Polygon | str, buffer_meters: int | None
) -> GeoDataFrame:
    tags = {
        "shop": ["convenience", "frozen_food", "greengrocer", "supermarket"],
    }
    gdf = get_pois_in_range(center, buffer_meters, tags)
    gdf["type"] = "convenience_store"
    return gdf


def get_restaurants_in_range(
    center: tuple[float, float] | Polygon | str, buffer_meters: int | None
) -> GeoDataFrame:
    tags = {
        "amenity": [
            "restaurant",
            "cafe",
            "fast_food",
            "food_court",
            "biergarten",
            "pub",
        ],
    }
    gdf = get_pois_in_range(center, buffer_meters, tags)
    gdf["type"] = "restaurant"
    return gdf


def get_gyms_in_range(
    center: tuple[float, float] | Polygon | str, buffer_meters: int | None
) -> GeoDataFrame:
    tags = {
        "leisure": [
            "fitness_centre",
            "fitness_station",
            "sports_hall",
            "sports_centre",
        ],
        "sport": ["fitness"],
        "building": ["sports_hall"],
    }
    gdf = get_pois_in_range(center, buffer_meters, tags)
    gdf["type"] = "gym"
    return gdf


def get_water_in_range(
    center: tuple[float, float] | Polygon | str, buffer_meters: int | None
) -> GeoDataFrame:
    tags = {
        "natural": ["beach"],
        "leisure": ["bathing_place"],
    }
    gdf = get_pois_in_range(center, buffer_meters, tags)
    gdf["type"] = "water"
    return gdf


if __name__ == "__main__":
    tags = {
        "amenity": ["restaurant", "pub", "hotel", "gym"],
        "building": "hotel",
        "tourism": "hotel",
    }
    north, east, south, west = 40.875, -73.910, 40.590, -74.080
    coords = [(west, south), (west, north), (east, north), (east, south), (west, south)]
    polygon = Polygon(coords)
    #    gdf = get_pois_in_range((34.0483, -118.2531), 500, tags)
    #    gdf = get_pois_in_range('Hallenborgs gata 4, Malmö, Sweden', 500, tags)
    # gdf = get_pois_in_range(polygon, 500, tags)
    # gdf = get_bus_stops_in_range((55.7063, 13.1996), 800)
    # gdf = get_convenience_stores_in_range((55.7063, 13.1996), 800)
    # gdf = get_restaurants_in_range((55.7063, 13.1996), 800)
    gdf = get_gyms_in_range((55.7091, 13.2017), 800)
    # gdf = get_water_in_range((55.6696, 13.0627), 800)
    print(gdf.head(20))
    #    print(gdf["name"])
    print(get_tag_dict())
