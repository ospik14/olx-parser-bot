from sqlalchemy.ext.asyncio import AsyncSession
from models.tables_models import Advertisement, SearchTask

async def create_new_search_task(db: AsyncSession, search: SearchTask):
    db.add(search)
    await db.commit()

async def create_advert(db: AsyncSession, adverts: list[Advertisement]):
    db.add(adverts)
    await db.commit()
