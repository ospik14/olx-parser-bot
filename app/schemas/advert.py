from pydantic import BaseModel

class AdsResponse(BaseModel):
    id: int
    title: str
    image_url: str | None
    price: str
    location: str
    date: str
    advert_url: str