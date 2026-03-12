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

        with open("olx_html_dump.html", "w", encoding="utf-8") as f:
            f.write(response.text)

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

            print(f"--- Оголошення ---")
            print(f"Назва: {ad.get('name')}")
            print(f"Ціна: {ad.get('price')} UAH")
            print(f"Локація: {ad.get('areaServed', {}).get('name', 'Невідомо')}")
            print(f"Посилання: {ad.get('url')}")
            print(f"Головне фото: {ad.get('image')[0] or None}")
            print("-" * 25)

            adverts[link] = AdsResponse (                   
                    title = title,
                    image_url = image_url,
                    price = str(price),
                    location = location,
                    advert_url = link
                )
        


asyncio.run(olx_request('https://www.olx.ua/uk/moda-i-stil/muzhskaya-odezhda/futbolki-mayki/futbolki/?currency=UAH'))