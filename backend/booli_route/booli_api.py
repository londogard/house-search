from typing import Any, Literal

from pydantic import BaseModel

# https://www.booli.se/p/api/referens
CORE_URL = "https://www.booli.se/api/proxy" # https://api.booli.se/listings?...
LISTINGS_URL = f"{CORE_URL}?url=/listings"


class Query(BaseModel):
    query: str | None = None
    center_coordinate: tuple[float, float] | None = None
    dim: str | None = None
    price_interval: tuple[float | None, float | None] | None = None
    area_id: str | None = None
    rooms: tuple[float | None, float | None] | None = None
    price: tuple[float | None, float | None] | None = None
    price_sqm: tuple[float | None, float | None] | None = None
    living_area: tuple[float | None, float | None] | None = None
    plot_area: tuple[float | None, float | None] | None = None
    object_type: list[Literal["villa", "lägenhet", "gård", "tomt-mark", "fritidshus", "parhus", "radhus", "kedjehus"]] | None = None
    construction_year: tuple[int | None, int | None] | None = None
    only_price_decreased: bool = False
    is_new_construction: bool | None = None
    limit: int | None = None
    offset: int | None = None

    def interval_matcher(self, interval: tuple | None, _from: str, _to: str, params: str) -> str:
        match interval:
            case [None, None]:
                pass
            case [None, _max]:
                params += f"&{_to}={_max}"
            case [_min, None]:
                params += f"&{_from}={_min}"
            case [_min, _max]:
                params += f"&{_from}={_min}&{_to}={_max}"

        return params

    def build_params(self) -> str:
        params = ""
        if self.query is not None:
            params += f"&q={self.query}"
        if self.center_coordinate is not None:
            params += f"&center={self.center_coordinate[0]},{self.center_coordinate[1]}"
        if self.dim is not None:
            params += f"&dim={self.dim}"
        params = self.interval_matcher(self.price_interval, "minListPrice", "maxListPrice", params)
        if self.area_id is not None:
            params += f"&areaId={self.area_id}"
        params = self.interval_matcher(self.rooms, "minRooms", "maxRooms", params)
        params = self.interval_matcher(self.price, "minListPrice", "maxListPrice", params)
        params = self.interval_matcher(self.price_sqm, "minListSqmPrice", "maxListSqmPrice", params)
        params = self.interval_matcher(self.living_area, "minLivingArea", "maxLivingArea", params)
        params = self.interval_matcher(self.plot_area, "minPlotArea", "maxPlotArea", params)
        params = self.interval_matcher(self.construction_year, "minConstructionYear", "maxConstructionYear", params)

        if self.object_type is not None:
            params += f"&objectType={','.join(self.object_type)}"

        if self.only_price_decreased:
            params += "&priceDecrease=1"

        if self.is_new_construction is not None:
            params += f"&isNewConstruction=1"

        if self.limit is not None:
            params += f"&limit={self.limit}"

        if self.offset is not None:
            params += f"&offset={self.offset}"

        return params[1:]   # remove first &

class Source(BaseModel):
    id: int
    url: str
    type: str
    name: str

class Address(BaseModel):
    city: str | None = None
    streetAddress: str | None = None

class Position(BaseModel):
    latitude: float
    longitude: float

class Region(BaseModel):
    countyName: str
    municipalityName: str

class Location(BaseModel):
    address: Address
    position: Position
    region: Region
    namedAreas: list[str]

class PropertyResponse(BaseModel):
    source: Source
    rooms: int
    hasPatio: int
    hasSolarPanels: int
    hasFireplace: int
    livingArea: int
    listPrice: int
    booliId: int
    objectType: str
    hasBalcony: int
    published: str
    biddingOpen: int
    url: str
    constructionYear: int | None = None
    location: Location | None = None
    additionalArea: int | None = None
    rent: int | None = None
    floor: str | None = None

class QueryResponse(BaseModel):
    limit: int
    offset: int
    listings: list[PropertyResponse]
    totalCount: int
    count: int
    searchParams: Any