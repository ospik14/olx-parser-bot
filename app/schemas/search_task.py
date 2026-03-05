from pydantic import BaseModel
from datetime import datetime

class SearchTaskResponse(BaseModel):
    id: int
    search_link: str
    owner_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

