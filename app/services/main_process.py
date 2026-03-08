import asyncio
from repositories.ads import get_premium_active_searches, get_all_active_searches
from services.advert_se import find_new_ads
from core.database import AsyncSessionLocal
from playwright.async_api import async_playwright


async def pars_loop():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        sem = asyncio.Semaphore(5)
        pars_count = 0
        while True:
            async with AsyncSessionLocal() as db:
                if pars_count == 8:
                    searches = await get_all_active_searches(db)
                    pars_count = 0
                else:
                    searches = await get_premium_active_searches(db)
                    pars_count += 1
  
                tasks = [
                    find_new_ads(sem, search, browser)
                    for search in searches
                ]
                await asyncio.gather(*tasks, return_exceptions=True)

            await asyncio.sleep(120)