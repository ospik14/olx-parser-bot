from models.tables_models import SearchTask
from parsers.olx_parser import search_for_ads
from repositories.ads import create_new_search_task, get_ads_id

async def add_new_search_link(db, link: str, user_id: str):
    search = SearchTask(search_link=link, owner_id=user_id)
    await create_new_search_task(db, search)


async def record_new_ads(db, search_url: str, search_id: int):
    ads = await search_for_ads(search_url)
    current_ads: set = await get_ads_id(db, search_id, ads)