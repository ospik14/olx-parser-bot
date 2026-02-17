from aiogram import Router, types, F
from aiogram.filters import CommandStart
from texts.message_texts import COMMAND_START, SEARCHES_LIMIT, NEW_SEARCHES
from services.advert_se import add_new_search_link
from models.tables_models import User
from repositories.users import create_user
from core.exceptions import LimitExceeded

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    await create_user(
        User(
            id=user_id, 
            username=username, 
            max_searches=3
        )
    )

    await message.answer(COMMAND_START.format(username=username))

@router.message(F.text.contains('https://www.olx.ua'))
async def new_search_link(message: types.Message):
    link = message.text
    user_id = message.from_user.id
    try:
        await add_new_search_link(link, user_id)
        await message.answer(NEW_SEARCHES)
    except LimitExceeded:
        await message.answer(SEARCHES_LIMIT)

    
