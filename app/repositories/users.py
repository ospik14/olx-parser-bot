from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import AsyncSessionLocal
from models.tables_models import User

async def create_user(user: User):
    async with AsyncSessionLocal() as db:
        try:
            db.add(user)
            await db.commit()
        except IntegrityError:
            return
        
async def get_user(db: AsyncSession, user_id: int):
    query = (select(User).where(User.id == user_id))
    user = await db.execute(query)

    return user.scalars().first()