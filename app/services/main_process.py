import asyncio
from app.repositories.ads import get_active_searches
from app.services.advert_se import find_new_ads
from app.core.database import AsyncSessionLocal
from playwright.async_api import async_playwright


async def pars_loop():
    while True:
        
        async with AsyncSessionLocal() as db:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                searches = await get_active_searches(db)

                sem = asyncio.Semaphore(5)
                tasks = [
                    find_new_ads(sem, db, search, browser)
                    for search in searches
                ]
        
                await asyncio.gather(*tasks, return_exceptions=True)

                
        await asyncio.sleep(120)