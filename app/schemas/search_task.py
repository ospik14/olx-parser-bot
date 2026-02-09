from pydantic import BaseModel

class CreateSearchTask(BaseModel):
    search_link: str
    user_id: str