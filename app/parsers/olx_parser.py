from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from playwright.async_api import async_playwright, Browser
from schemas.advert import AdsResponse

async def improve_link(url: str):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    query_params['search[order]'] = ['created_at:desc']

    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))

    return new_url

async def search_for_ads(page_link, browser: Browser):
    context = await browser.new_context()

    page = await context.new_page()
    await page.goto(page_link)

    await page.keyboard.press('Enter')

    await page.wait_for_selector('[data-testid="listing-grid"]')
    advert_grid = page.get_by_test_id('listing-grid').first

    cards = await advert_grid.get_by_test_id('l-card').all()
    adverts: dict[int, AdsResponse] = {}
    for card in cards:
        await card.scroll_into_view_if_needed()
        id = await card.get_attribute('id')
        image = await card.locator('img').get_attribute('src')
        title = await card.locator('h4').inner_text()
        price = await card.locator('[data-testid="ad-price"]').inner_text()
        location_date = await card.locator('[data-testid="location-date"]').inner_text()
        link_part = await card.locator('[data-testid="ad-card-title"] a').get_attribute('href')
        full_link = f'https://www.olx.ua{link_part}'

        adverts[int(id)] = AdsResponse (                   
                id = int(id),
                title = title,
                image_url = image,
                price = price,
                location_and_date = location_date,
                advert_url = full_link
            )
            
    await context.close()

    return adverts
    
    
