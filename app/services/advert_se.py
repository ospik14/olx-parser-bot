from models.tables_models import SearchTask, Advertisement
from parsers.olx_parser import search_for_ads
from repositories.ads import create_new_search_task, get_ads_id, create_ads

async def add_new_search_link(db, link: str, user_id: str):
    search = SearchTask(search_link=link, owner_id=user_id)
    await create_new_search_task(db, search)


async def find_new_ads(db, search_url: str, search_id: int):
    ads: dict = await search_for_ads(search_url)
    exist_ads: set = await get_ads_id(db, search_id, ads)
    to_save = [ads[id] for id in (ads.keys() - exist_ads)]

    new_ads = [Advertisement(**ad.model_dump()) for ad in to_save]
    await create_ads(db, new_ads)
