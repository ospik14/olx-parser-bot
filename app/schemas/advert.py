from pydantic import BaseModel

class AdsResponse(BaseModel):
    title: str
    image_url: str | None
    price: str
    location: str
    advert_url: str