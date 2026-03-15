import json
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup
from curl_cffi import AsyncSession
from schemas.advert import AdsResponse


def improve_link(url: str, param: dict):
    parsed_url = urlparse(url)
    query_params: dict = parse_qs(parsed_url.query)

    query_params.update(param)

    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))

    return new_url

async def intercept_route(route):
    if route.request.resource_type in ['media', 'font']:
        await route.abort()
    else:
        await route.continue_()

async def search_for_ads(page_link: str):
    async with AsyncSession(impersonate='chrome120') as session:
        print('pars start')

        response = await session.get(page_link)  

        if response.status_code != 200: 
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        additional_data_map = {}
        ad_cards = soup.find_all('div', {'data-testid': 'l-card'})
        for card in ad_cards:
            link_tag = card.find('a', href=True)
            loc_tag = card.find('p', {'data-testid': 'location-date'})
            price_tag = card.find('p', {'data-testid': 'ad-price'})

            if link_tag and loc_tag and price_tag:
                raw_url = link_tag['href'].split('?')[0]
                ad_url = f"https://www.olx.ua{raw_url}" if raw_url.startswith('/') else raw_url

                full_loc_text = loc_tag.text.strip()
                clean_location = full_loc_text.split(' - ')[0]
                price_text = price_tag.text.strip()

                additional_data_map[ad_url] = {'loc': clean_location, 'price': price_text}


        script_tag = soup.find_all('script', type='application/ld+json')

        if not script_tag:
            print('NOT SCRIPT')
            print(response.text[:500])
            return

        ads_list = []
        for script in script_tag:
            try:
                data: dict = json.loads(script.string)

                if data.get('@type') == 'Product' and 'offers' in data:
                    ads_list = data['offers'].get('offers', [])
                    break
            except (json.JSONDecodeError, TypeError):
                continue

        
        adverts: dict[str, AdsResponse] = {}
        for ad in ads_list:
            image_url = ad.get('image')[0] or None
            title = ad.get('name')
            price = ad.get('price')
            location = ad.get('areaServed', {}).get('name', 'Невідомо')
            link = ad.get('url')


            adverts[link] = AdsResponse (                   
                    title = title,
                    image_url = image_url,
                    price = additional_data_map.get(link).get('price') or price,
                    location = additional_data_map.get(link).get('loc') or location,
                    advert_url = link
                ) 
        print('pars done')

        return adverts
        
    
    
