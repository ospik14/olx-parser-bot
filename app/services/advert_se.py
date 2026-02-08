from app.models.tables_models import SearchTask
from parser import search_for_ads
from repositories.ads import create_new_search_task

async def add_new_search_link(db, link: str, user_id: int):
    search = SearchTask(search_link=link, owner_id=user_id)
    await create_new_search_task(db, search)


async def record_new_ads(db, search_url: str):
    await search_for_ads(search_url)