from fastapi import APIRouter
from dependencies import db_dep
from services.advert_se import add_new_search_link

router = APIRouter()

@router.get('/search-url/')
async def create_search_task(db: db_dep, search_url: str, user_id: int):
    await add_new_search_link(db, search_url, user_id)