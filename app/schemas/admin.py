from pydantic import BaseModel

class StatsBase(BaseModel):
    users: int
    searches: int