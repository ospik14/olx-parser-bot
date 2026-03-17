from core.database import AsyncSessionLocal
from repositories.admin import get_users_count, get_searches_count
from schemas.admin import StatsBase

async def collect_statistics():
    async with AsyncSessionLocal() as db:
        users = await get_users_count(db)
        searches = await get_searches_count(db)
        stats = StatsBase(users=users, searches=searches)

        return stats