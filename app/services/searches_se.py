from datetime import datetime, timezone
from schemas.search_task import SearchTaskResponse
from models.tables_models import SearchTask
from core.exceptions import LimitExceeded, SearchExists
from repositories.searches import create_new_search_task, delete_search, \
get_search_for_id, get_searches_count, get_searches_for_user, \
update_search_status, get_search_by_link
from core.database import AsyncSessionLocal
from repositories.users import get_user


async def add_new_search_link(link: str, user_id: str):
    async with AsyncSessionLocal() as db:
        user = await get_user(db, user_id)
        count_of_searches = await get_searches_count(db, user_id)
        is_link_exists = await get_search_by_link(db, link)

        if not is_link_exists:
            raise SearchExists

        if user.premium_expires_at < datetime.now(timezone.utc):
            if count_of_searches >= 3:
                raise LimitExceeded
        
        search = SearchTask(search_link=link, owner_id=user_id)
        await create_new_search_task(search)

async def get_my_searches(user_id: int):
    async with AsyncSessionLocal() as db:
        searches = await get_searches_for_user(db, user_id)

        return [
            SearchTaskResponse.model_validate(search)
            for search in searches
        ]
    
async def change_status_in_search(search_id: int, user_id: int):
    async with AsyncSessionLocal() as db:

        user = await get_user(db, user_id)
        search = await get_search_for_id(db, search_id)
        count_of_searches = await get_searches_count(db, user_id)

        if user.premium_expires_at < datetime.now(timezone.utc):
            if not search.is_active and count_of_searches >= 3:
                raise LimitExceeded
        
        await update_search_status(db, search_id)

        await db.commit()
        await db.refresh(search)

        return SearchTaskResponse.model_validate(search)
    
async def clean_search(search_id: int):
    async with AsyncSessionLocal() as db:
        try:
            await delete_search(db, search_id)
        except Exception:
            return

