import asyncio
from repositories.ads import get_active_searches
from services.advert_se import find_new_ads
from core.database import AsyncSessionLocal, get_session ##


async def pars_loop():
    while True:
        
        async with AsyncSessionLocal() as db:
            searches = await get_active_searches(db)
            sem = asyncio.Semaphore(5)

            tasks = [
                find_new_ads(sem, db, search.search_link, search.owner_id)
                for search in searches
            ]
        
        await asyncio.gather(*tasks)
        await asyncio.sleep(120)