from models.tables_models import SearchTask
from parsers.olx_parser import search_for_ads, improve_link
from repositories.ads import create_new_search_task, get_ads_id, create_ads, create_searches_ads

async def add_new_search_link(db, link: str, user_id: str):
    search = SearchTask(search_link=link, owner_id=user_id)
    await create_new_search_task(db, search)


async def find_new_ads(sem, db, search_url: str, search_id: int, browser):
    improved_link = await improve_link(search_url)
    ads: dict = await search_for_ads(improved_link, browser)
    exist_ads: set = await get_ads_id(db, search_id, ads)
    to_save = [ads[id] for id in (ads.keys() - exist_ads)]
    if not to_save: return 
    print('A'*50)

    gg = [t.id for t in to_save]
    print(gg)
    print('A'*50)

    new_ads = [ad.model_dump() for ad in to_save]
    await create_ads(db, new_ads)

    search_ads = [
        {'ads_id': s_ad.id, 'search_id': search_id }
        for s_ad in to_save
    ]
    await create_searches_ads(db, search_ads)

    print(new_ads)