import asyncio
import json
from curl_cffi.requests import AsyncSession
from bs4 import BeautifulSoup

from app.schemas.advert import AdsResponse

async def olx_request(url: str):
    async with AsyncSession(impersonate='chrome120') as session:
        response = await session.get(url)  

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

        

        for ad in ads_list:
            image_url = ad.get('image')[0] or None
            title = ad.get('name')
            price = ad.get('price')
            location = ad.get('areaServed', {}).get('name', 'Невідомо')
            link = ad.get('url')

            print(f"--- Оголошення ---")
            print(f"Назва: {ad.get('name')}")
            print(f"Ціна: {additional_data_map.get(link).get('price')}")
            print(f"Локація: {additional_data_map.get(link).get('loc')}")
            print(f"Посилання: {ad.get('url')}")
            print(f"Головне фото: {ad.get('image')[0] or None}")
            print("-" * 25)

            
        


asyncio.run(olx_request('https://www.olx.ua/uk/nedvizhimost/kvartiry/prodazha-kvartir/lvov/?currency=UAH&search%5Bfilter_float_floor:from%5D=4&search%5Bfilter_float_floor:to%5D=8&search%5Bfilter_enum_apartments_object_type%5D%5B0%5D=secondary_market'))