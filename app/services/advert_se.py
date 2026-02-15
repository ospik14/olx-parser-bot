import asyncio
from datetime import datetime, timezone, timedelta
from core.database import AsyncSessionLocal
from models.tables_models import SearchTask
from parsers.olx_parser import search_for_ads, improve_link
from repositories.ads import create_new_search_task, get_ads_id, create_ads, create_searches_ads
from services.notification import return_new_ads

async def add_new_search_link(link: str, user_id: str):
    search = SearchTask(search_link=link, owner_id=str(user_id))
    await create_new_search_task(search)

async def find_new_ads(sem: asyncio.Semaphore, search: SearchTask, browser):
    async with sem:
        async with AsyncSessionLocal() as db:
            time_since_creation = datetime.now(timezone.utc) - search.created_at
            is_warmup_mode = time_since_creation < timedelta(minutes=10)

            improved_link = improve_link(search.search_link, {'search[order]':'created_at:desc'})
            ads: dict = await search_for_ads(improved_link, browser)

            if is_warmup_mode: 
                two_page_link = improve_link(improved_link, {'page':2})
                ads_page_2: dict = await search_for_ads(two_page_link, browser)
                ads.update(ads_page_2)

            exist_ads: set = await get_ads_id(db, search.id, ads)
            to_save = [ads[id] for id in (ads.keys() - exist_ads)]
            if not to_save: return 

            new_ads = [ad.model_dump() for ad in to_save]
            search_ads = [
                {'ads_id': s_ad.id, 'search_id': search.id }
                for s_ad in to_save
            ]
            try:
                await create_ads(db, new_ads)
                await create_searches_ads(db, search_ads)
            except Exception:
                return

            
            
            if not is_warmup_mode:
                await return_new_ads({'user_id': search.owner_id, 'ads': new_ads})