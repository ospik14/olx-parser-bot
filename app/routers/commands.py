from fastapi import APIRouter
from dependencies import db_dep
from services.advert_se import add_new_search_link
from schemas.search_task import CreateSearchTask

router = APIRouter()

@router.post('/search-url/')
async def create_search_task(db: db_dep, search: CreateSearchTask):
    await add_new_search_link(db, search.search_link, search.user_id)
    