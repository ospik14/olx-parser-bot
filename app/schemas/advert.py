from pydantic import BaseModel

class AdsResponse(BaseModel):
    advert_id: int
    title: str
    image_ur: str
    price: float
    location_and_date: str
    advert_url: str