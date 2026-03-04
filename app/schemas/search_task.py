from pydantic import BaseModel
from datetime import datetime

class SearchTaskBase(BaseModel):
    search_link: str
    user_id: int

class CreateSearchTask(SearchTaskBase):
    pass

class SearchTaskResponse(SearchTaskBase):
    id: int
    owner_id: int
    is_active: bool
    created_at: datetime

