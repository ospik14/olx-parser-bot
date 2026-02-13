from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tables_models import Advertisement, SearchTask, SearchAd

async def create_new_search_task(db: AsyncSession, search: SearchTask):
    db.add(search)
    await db.commit()

async def get_active_searches(db: AsyncSession):
    query = (
        select(SearchTask)
        .where(SearchTask.is_active == True)
    )
    searches = await db.execute(query)

    return searches.scalars().all()

async def get_ads_id(db: AsyncSession, search_id: int, ads_id: set):
    query = (
        select(SearchAd.ads_id)
        .where(SearchAd.search_id == search_id)
        .where(SearchAd.ads_id.in_(ads_id))
    )
    ads = await db.execute(query)

    return set(ads.scalars().all())

async def create_ads(db: AsyncSession, adverts: list[dict]):
    stmt = (
        insert(Advertisement).values(adverts)
        .on_conflict_do_nothing(index_elements=['id'])
    )
    
    await db.execute(stmt)
    await db.commit()

async def create_searches_ads(db: AsyncSession, s_ads: list[dict]):
    stmt = (insert(SearchAd).values(s_ads))
    await db.execute(stmt)
    await db.commit()

