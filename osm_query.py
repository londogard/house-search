from geopandas import GeoDataFrame
from shapely.geometry import Point, box, Polygon
from typing import Any
import osmnx as ox
import os
os.environ['USE_PYGEOS'] = '0'


ox.config(log_console=True, use_cache=True)


def get_pois_in_range(center: tuple[float, float] | Polygon, buffer_meters: int | None, tags: dict[str, Any]) -> GeoDataFrame:
    match center:
        # additionally exists like _from_address, _from_place, ...
        case tuple():
            print("HEHE", center)
            return ox.geometries_from_point(center, dist=buffer_meters, tags=tags)
        case Polygon():
            print("HOHO")
            return ox.geometries_from_polygon(center, tags=tags)


if __name__ == '__main__':
    tags = {
        'amenity': ['restaurant', 'pub', 'hotel'],
        'building': 'hotel',
        'tourism': 'hotel'
    }
    gdf = get_pois_in_range((34.0483, -118.2531), 500, tags)
    print(gdf.head())
