import asyncio
from datetime import datetime, timezone, timedelta
from core.database import AsyncSessionLocal
from models.tables_models import SearchTask
from parsers.olx_parser import search_for_ads, improve_link
from repositories.ads import get_ads_link, create_ads, create_searches_ads
from services.notification import return_new_ads


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

