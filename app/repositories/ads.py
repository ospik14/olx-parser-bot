from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.tables_models import Advertisement, SearchTask, SearchAd

async def create_new_search_task(db: AsyncSession, search: SearchTask):
    db.add(search)
    await db.commit()

async def get_ads_id(db: AsyncSession, search_id: int, ads_id: set):
    query = (
        select(SearchAd.ads_id)
        .where(SearchAd.search_id == search_id)
        .where(SearchAd.ads_id in ads_id)
    )
    ads = await db.execute(query)

    return ads.scalars().all()

async def create_advert(db: AsyncSession, adverts: list[Advertisement]):
    db.add(adverts)
    await db.commit()
