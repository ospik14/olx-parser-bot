from aiogram import Router, types, F
from aiogram.filters import CommandStart
from texts.message_texts import COMMAND_START
from services.advert_se import add_new_search_link

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(COMMAND_START)

@router.message(F.text.contains('https://www.olx.ua'))
async def new_search_link(message: types.Message):
    link = message.text
    user_id = message.from_user.id
    
    await add_new_search_link(link, user_id)

    await message.answer('Посилання додано, очікуйте сповіщення про нові оголошення')
