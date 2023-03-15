from geopandas import GeoDataFrame
from shapely.geometry import Point, box, Polygon
from typing import Any
import osmnx as ox
import os
os.environ['USE_PYGEOS'] = '0'


ox.config(log_console=True, use_cache=True)


def get_pois_in_range(center: tuple[float, float] | Polygon | str, buffer_meters: int | None, tags: dict[str, Any]) -> GeoDataFrame:
    match center:
        # additionally exists like _from_address, _from_place, ...
        case tuple():
            print("HEHE", center)
            return ox.geometries_from_point(center, dist=buffer_meters, tags=tags)
        case Polygon():
            print("HOHO")
            return ox.geometries_from_polygon(center, tags=tags)
        case str():
            print("place")
            return ox.geometries_from_place(center, tags=tags)


def get_bus_stops_in_range(center: tuple[float, float] | Polygon | str, buffer_meters: int | None) -> GeoDataFrame:
    tags = {
               "public_transport": ["stop_position", "platform", "station", "stop_area"],
               "railway": ["rail", "subway", "tram", "light_rail", "monorail", "monorail_service"],
               "amenity": ["bus_station", "bicycle_rental"],
    }
    gdf = get_pois_in_range(center, buffer_meters, tags)
    return gdf


def get_convenience_stores_in_range(center: tuple[float, float] | Polygon | str, buffer_meters: int | None) -> GeoDataFrame:
    tags = {
               "shop": ["convenience", "frozen_food", "greengrocer", "supermarket"],
    }
    gdf = get_pois_in_range(center, buffer_meters, tags)
    return gdf


def get_restaurants_in_range(center: tuple[float, float] | Polygon | str, buffer_meters: int | None) -> GeoDataFrame:
    tags = {
               "amenity": ["restaurant", "cafe", "fast_food", "food_court", "biergarten", "pub"],
    }
    gdf = get_pois_in_range(center, buffer_meters, tags)
    return gdf


def get_gyms_in_range(center: tuple[float, float] | Polygon | str, buffer_meters: int | None) -> GeoDataFrame:
    tags = {
               "leisure": ["fitness_centre", "fitness_station", "sports_hall", "sports_centre"],
               "sport": ["fitness"],
               "building": ["sports_hall"]
    }
    gdf = get_pois_in_range(center, buffer_meters, tags)
    return gdf


def get_water_in_range(center: tuple[float, float] | Polygon | str, buffer_meters: int | None) -> GeoDataFrame:
    tags = {
               "natural": ["beach"],
               "leisure": ["bathing_place"],
    }
    gdf = get_pois_in_range(center, buffer_meters, tags)
    return gdf

if __name__ == '__main__':
    tags = {
        'amenity': ['restaurant', 'pub', 'hotel', 'gym'],
        'building': 'hotel',
        'tourism': 'hotel',
 
    }
    north, east, south, west = 40.875, -73.910, 40.590, -74.080
    coords = [(west, south),(west, north),(east,north),(east, south), (west, south)]
    polygon = Polygon(coords)
#    gdf = get_pois_in_range((34.0483, -118.2531), 500, tags)
#    gdf = get_pois_in_range('Hallenborgs gata 4, Malmö, Sweden', 500, tags)
    #gdf = get_pois_in_range(polygon, 500, tags)
    #gdf = get_bus_stops_in_range((55.7063, 13.1996), 800)
    #gdf = get_convenience_stores_in_range((55.7063, 13.1996), 800)
    #gdf = get_restaurants_in_range((55.7063, 13.1996), 800)
    gdf = get_gyms_in_range((55.7091, 13.2017), 800)
    #gdf = get_water_in_range((55.6696, 13.0627), 800)
    print(gdf.head(20))
#    print(gdf["name"])
