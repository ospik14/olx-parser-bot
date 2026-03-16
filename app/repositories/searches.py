from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, func, not_, or_, select, update
from models.tables_models import SearchTask, User
from core.database import AsyncSessionLocal

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

async def get_all_active_searches(db: AsyncSession):
    query = (
        select(SearchTask)
        .where(SearchTask.is_active == True)
    )
    searches = await db.execute(query)

    return searches.scalars().all()
    
async def get_priority_active_searches(db: AsyncSession):
    now_time = datetime.now(timezone.utc)
    query = (
        select(SearchTask)
        .join(SearchTask.user)
        .where(
            SearchTask.is_active == True,
            or_(
                User.premium_expires_at > now_time,
                now_time - SearchTask.activated_at < timedelta(minutes=10)
            )
        )
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

async def get_search_for_id(db: AsyncSession, id: int):
    query = (select(SearchTask).where(SearchTask.id == id))
    search = await db.execute(query)

    return search.scalar_one_or_none()

async def update_search_status(db: AsyncSession, id: int):
    stmt = (
        update(SearchTask)
        .where(SearchTask.id == id)
        .values(
            is_active = not_(SearchTask.is_active),
            activated_at = func.now()
        )
    )
    await db.execute(stmt)
    
async def delete_search(db: AsyncSession, id: int):
    stmt = (
        delete(SearchTask).where(SearchTask.id == id)
    )
    await db.execute(stmt)
    await db.commit()

async def get_users_searches_count(db: AsyncSession):
    query = (
        select(
            SearchTask.owner_id.label('user_id'), 
            func.count(SearchTask.id).label('searches_count')
        )
        .join(SearchTask.user)
        .where(
            SearchTask.is_active == True,
            User.premium_expires_at < datetime.now(timezone.utc)
        )
        .group_by(SearchTask.owner_id)
    )
    result = await db.execute(query)

    return result.all()

async def deactivate_searches(db: AsyncSession, user_id: int):
    stmt = (
        update(SearchTask)
        .where(SearchTask.owner_id == user_id)
        .values(is_active = False)
    )
    await db.execute(stmt)

async def get_search_by_link(db: AsyncSession, link: str):
    query = (select(SearchTask).where(SearchTask.search_link == link))
    search = await db.execute(query)

    return search.scalar_one_or_none()