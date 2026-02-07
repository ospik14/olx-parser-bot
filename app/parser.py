import asyncio
from playwright.async_api import async_playwright
from dependencies import db_dep
from models.tables_models import Advertisement

async def test_run(db: db_dep):
    async with async_playwright() as p:
        page_link = 'https://www.olx.ua'

        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        page = await browser.new_page()
        await page.goto(f'{page_link}/uk')

        await page.fill('input[id="search"]', 'Samsung a20')
        await page.keyboard.press('Enter')

        await page.wait_for_selector('[data-testid="listing-grid"]')

        cards = await page.locator('[data-testid="l-card"]').all()
        for card in cards:
            await card.scroll_into_view_if_needed()
            id = await card.get_attribute('id')
            image = await card.locator('img').get_attribute('src')
            title = await card.locator('h4').inner_text()
            price = await card.locator('[data-testid="ad-price"]').inner_text()
            location_date = await card.locator('[data-testid="location-date"]').inner_text()
            link_part = await card.locator('[data-testid="ad-card-title"] a').get_attribute('href')
            full_link = f'{page_link}{link_part}'

            print(f'id: {id}')
            print(f'image: {image}')
            print(f'назва: {title}')
            print(f'ціна: {price}')
            print(f'локація і дата: {location_date}')
            print(f'посилання: {full_link}')
            print(" ")

            #advert = Advertisement(                    WRONG!
            #    advert_id = id,
            #    title = title,
            #   image_url = image,
            #   price = price,
            #    location_and_date = location_date,
            #    advert_url = full_link
            #)
            #db.add(advert)
            #await db.commit()

        await browser.close()
    
asyncio.run(test_run())
