import asyncio
from datetime import datetime, timezone, timedelta
from core.database import AsyncSessionLocal
from models.tables_models import SearchTask
from parsers.olx_parser import search_for_ads, improve_link
from repositories.ads import create_new_search_task, get_ads_link, create_ads, \
create_searches_ads, get_searches_count, get_searches_for_user, \
get_search_for_id, update_search_status, delete_search
from repositories.users import get_user
from services.notification import return_new_ads
from core.exceptions import LimitExceeded
from schemas.search_task import SearchTaskResponse

async def add_new_search_link(link: str, user_id: str):
    async with AsyncSessionLocal() as db:
        user = await get_user(db, user_id)
        count_of_searches = await get_searches_count(db, user_id)

        if user.premium_expires_at < datetime.now(timezone.utc):
            if count_of_searches >= 3:
                raise LimitExceeded
        
        search = SearchTask(search_link=link, owner_id=user_id)
        await create_new_search_task(search)

async def get_my_searches(user_id: int):
    async with AsyncSessionLocal() as db:
        searches = await get_searches_for_user(db, user_id)

        return [
            SearchTaskResponse.model_validate(search)
            for search in searches
        ]

async def find_new_ads(sem: asyncio.Semaphore, search: SearchTask):
    async with sem:
        async with AsyncSessionLocal() as db:
            time_since_creation = datetime.now(timezone.utc) - search.activated_at
            is_warmup_mode = time_since_creation < timedelta(minutes=10)

            improved_link = improve_link(search.search_link, {'search[order]':'created_at:desc'})
            ads: dict = await search_for_ads(improved_link)
            if not ads: return

            exist_ads: set = await get_ads_link(db, search.id, ads.keys())
            print(f"AD_URL_SAMPLE: {list(ads.keys())[0] if ads else 'EMPTY'}")
            print(f"EXIST_URL_SAMPLE: {list(exist_ads)[0] if exist_ads else 'EMPTY'}")
            to_save = [ads[link] for link in (ads.keys() - exist_ads)]
            if not to_save: return 

            new_ads = [ad.model_dump() for ad in to_save]
            search_ads = [
                {'advert_url': s_ad.advert_url, 'search_id': search.id }
                for s_ad in to_save
            ]
            try:
                await create_ads(db, new_ads)
                await create_searches_ads(db, search_ads)
                await db.commit()
            except Exception:
                return

            
            if not is_warmup_mode:
                await return_new_ads({'user_id': search.owner_id, 'ads': new_ads})

async def change_status_in_search(search_id: int, user_id: int):
    async with AsyncSessionLocal() as db:

        user = await get_user(db, user_id)
        search = await get_search_for_id(db, search_id)
        count_of_searches = await get_searches_count(db, user_id)

        if user.premium_expires_at < datetime.now(timezone.utc):
            if not search.is_active and count_of_searches >= 3:
                raise LimitExceeded
        
        await update_search_status(db, search_id)

        await db.commit()
        await db.refresh(search)

        return SearchTaskResponse.model_validate(search)
    
async def clean_search(search_id: int):
    async with AsyncSessionLocal() as db:
        try:
            await delete_search(db, search_id)
        except Exception:
            return

