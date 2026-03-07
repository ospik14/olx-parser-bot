from sqlalchemy import not_, select, update, delete, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import AsyncSessionLocal
from models.tables_models import Advertisement, SearchTask, SearchAd

async def create_new_search_task(search: SearchTask):
    async with AsyncSessionLocal() as db:
        db.add(search)
        await db.commit()

async def get_searches_count(db: AsyncSession, user_id: int):
    query = (
        select(func.count())
        .select_from(SearchTask)
        .where(
            SearchTask.owner_id == user_id,
            SearchTask.is_active == True
        )
    )
    count = await db.execute(query)
    
    return count.scalar() or 0

async def get_active_searches():
    async with AsyncSessionLocal() as db:
        query = (
            select(SearchTask)
            .where(SearchTask.is_active == True)
        )
        searches = await db.execute(query)

        return searches.scalars().all()
    
async def get_searches_for_user(db: AsyncSession, user_id: int):
    query = (
        select(SearchTask)
        .where(
            SearchTask.owner_id == user_id,
        )
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

async def get_search_for_id(db: AsyncSession, id: int):
    query = (select(SearchTask).where(SearchTask.id == id))
    search = await db.execute(query)

    return search.scalar_one_or_none()

async def update_search_status(db: AsyncSession, id: int):
    stmt = (
        update(SearchTask)
        .where(SearchTask.id == id)
        .values(is_active = not_(SearchTask.is_active))
    )
    await db.execute(stmt)
    
async def delete_search(db: AsyncSession, id: int):
    stmt = (
        delete(SearchTask).where(SearchTask.id == id)
    )
    await db.execute(stmt)
    await db.commit()