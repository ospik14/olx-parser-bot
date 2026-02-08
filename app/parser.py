import asyncio
from playwright.async_api import async_playwright
from dependencies import db_dep
from models.tables_models import Advertisement
from app.repositories import ads

async def search_for_ads(page_link):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        page = await browser.new_page()
        await page.goto(page_link)

        await page.keyboard.press('Enter')

        await page.wait_for_selector('[data-testid="listing-grid"]')
        advert_grid = page.get_by_test_id('listing-grid').first

        cards = await advert_grid.get_by_test_id('l-card').all()
        adverts = [Advertisement]
        for card in cards:
            await card.scroll_into_view_if_needed()
            id = await card.get_attribute('id')
            image = await card.locator('img').get_attribute('src')
            title = await card.locator('h4').inner_text()
            price = await card.locator('[data-testid="ad-price"]').inner_text()
            location_date = await card.locator('[data-testid="location-date"]').inner_text()
            link_part = await card.locator('[data-testid="ad-card-title"] a').get_attribute('href')
            full_link = f'https://www.olx.ua{link_part}'
   
            adverts.append(
                Advertisement(                   
                    advert_id = id,
                    title = title,
                    image_url = image,
                    price = price,
                    location_and_date = location_date,
                    advert_url = full_link
                )
            )
        await browser.close()
    
