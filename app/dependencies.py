from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session

db_dep = Annotated[AsyncSession, get_session]