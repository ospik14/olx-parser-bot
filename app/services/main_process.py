import asyncio
from repositories.ads import get_active_searches
from advert_se import find_new_ads


async def pars_loop(db):

    while True:
        await asyncio.sleep(120)

        searches = await get_active_searches(db)
        sem = asyncio.Semaphore(5)

        tasks = [
            find_new_ads(sem, db, search.search_link, search.owner_id)
            for search in searches
        ]
        
        await asyncio.gather(*tasks)