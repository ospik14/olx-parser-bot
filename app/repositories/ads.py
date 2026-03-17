from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from models.tables_models import Advertisement, SearchAd


async def get_ads_link(db: AsyncSession, search_id: int, adverts_url: set):
    query = (
        select(SearchAd.advert_url)
        .where(SearchAd.search_id == search_id)
        .where(SearchAd.advert_url.in_(adverts_url))
    )
    ads = await db.execute(query)

    return set(ads.scalars().all())

async def create_ads(db: AsyncSession, adverts: list[dict]):
    stmt = (
        insert(Advertisement).values(adverts)
        .on_conflict_do_nothing(index_elements=['advert_url'])
    )
    await db.execute(stmt)

async def create_searches_ads(db: AsyncSession, s_ads: list[dict]):
    stmt = (insert(SearchAd).values(s_ads))
    await db.execute(stmt)


