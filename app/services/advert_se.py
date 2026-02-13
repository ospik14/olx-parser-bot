from app.models.tables_models import SearchTask
from app.parsers.olx_parser import search_for_ads, improve_link
from app.repositories.ads import create_new_search_task, get_ads_id, create_ads, create_searches_ads
from app.services.notification import return_new_ads

async def add_new_search_link(db, link: str, user_id: str):
    search = SearchTask(search_link=link, owner_id=user_id)
    await create_new_search_task(db, search)


async def find_new_ads(sem, db, search: SearchTask, browser):
    improved_link = improve_link(search.search_link)
    ads: dict = await search_for_ads(improved_link, browser)
    exist_ads: set = await get_ads_id(db, search.id, ads)
    to_save = [ads[id] for id in (ads.keys() - exist_ads)]
    if not to_save: return 

    new_ads = [ad.model_dump() for ad in to_save]
    await create_ads(db, new_ads)

    search_ads = [
        {'ads_id': s_ad.id, 'search_id': search.id }
        for s_ad in to_save
    ]
    await create_searches_ads(db, search_ads)

    await return_new_ads({'user_id': search.owner_id, 'ads': new_ads})