import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from loader import bot
from texts.message_texts import ADS_RESPONSE_TEXT

TZ_KYIV = ZoneInfo("Europe/Kyiv")

async def return_new_ads(ads_response: dict):
    user_id = ads_response.get('user_id')
    new_ads = ads_response.get('ads')

    for ad in new_ads:
        title = ad.get('title')
        price = ad.get('price')
        location = ad.get('location')
        advert_url = ad.get('advert_url')
        img_url = ad.get('image_url')

        caption = ADS_RESPONSE_TEXT.format(
            title=title,
            price=price,
            location=location,
            date=datetime.now(tz=TZ_KYIV),
            advert_url=advert_url,
        )

        try:
            if img_url.startswith('https'):
                await bot.send_photo(
                    chat_id=user_id, 
                    photo=img_url,
                    caption=caption,
                    parse_mode='HTML'
                )
            else:
                await bot.send_message(
                    chat_id=user_id, 
                    text=caption,
                    parse_mode='HTML'
                )
        except Exception as e:
            print(f"Не вдалося надіслати повідомлення юзеру {user_id}: {e}")


        
        await asyncio.sleep(0.3)