from fastapi import APIRouter

router = APIRouter(prefix="/booli/")
@dataclass
class Query:
    query: str | None = None
    center_coordinate: tuple[float, float] | None = None
    # https://www.booli.se/p/api/referens

@router.get("/query")
def get_temperature():
    temperature = sensor.get_temperature()
    return temperature