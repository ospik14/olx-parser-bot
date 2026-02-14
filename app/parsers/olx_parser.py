from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from playwright.async_api import Browser, TimeoutError, Error
from schemas.advert import AdsResponse

def improve_link(url: str):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    query_params['search[order]'] = ['created_at:desc']

    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))

    return new_url

async def intercept_route(route):
    if route.request.resource_type in ['image', 'media', 'font']:
        await route.abort()
    else:
        await route.continue_()

async def search_for_ads(page_link, browser: Browser):
    try:
        print('pars start')
        context = await browser.new_context(
            timezone_id='Europe/Kiev',
            locale='uk-Ua'
        )

        page = await context.new_page()
        await page.route('**/*', intercept_route)
        await page.goto(page_link, timeout=15000, wait_until='domcontentloaded')


        await page.wait_for_selector('[data-testid="listing-grid"]', timeout=10000)
        advert_grid = page.get_by_test_id('listing-grid').first

        cards = await advert_grid.get_by_test_id('l-card').all()
        adverts: dict[int, AdsResponse] = {}
        for card in cards:
            await card.scroll_into_view_if_needed()
            id = await card.get_attribute('id')
            image = await card.locator('img').first.get_attribute('srcset') or 'not'
            title = await card.locator('h4').inner_text()
            price = await card.locator('[data-testid="ad-price"]').inner_text()
            location_date = await card.locator('[data-testid="location-date"]').inner_text()
            link_part = await card.locator('[data-testid="ad-card-title"] a').get_attribute('href')
            full_link = f'https://www.olx.ua{link_part}'

            adverts[int(id)] = AdsResponse (                   
                    id = int(id),
                    title = title,
                    image_url = image.split(';')[0],
                    price = price,
                    location_and_date = location_date,
                    advert_url = full_link
                )
        print('pars done')
        return adverts
    
    except TimeoutError:
        print(f"Timeout: {page_link}")
        return {}
    except Error as e:
        print(f"Playwright Error: {e}")
        return {}
    except Exception:
        print(f"Code Error: {e}")
        return {}

    finally:
        await context.close()
    
    
