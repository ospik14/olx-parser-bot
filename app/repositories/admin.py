from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from models.tables_models import User, SearchTask

async def get_users_count(db: AsyncSession):
    query = (
        select(func.count())
        .select_from(User)
    )
    result = await db.execute(query)

    return result.scalar() or 0

async def get_searches_count(db: AsyncSession):
    query = (
        select(func.count())
        .select_from(SearchTask)
        .where(SearchTask.is_active == True)
    )
    result = await db.execute(query)

    return result.scalar() or 0