from aiogram import Router, types, F
from aiogram.filters import CommandStart
from bot.texts.message_texts import COMMAND_START
from bot.utils.api_request import create_searches_task

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(COMMAND_START)

@router.message(F.text.contains('https://www.olx.ua'))
async def new_search_link(message: types.Message):
    link = message.text
    user_id = message.from_user.id
    
    try:
        await create_searches_task(link, user_id)
    except Exception:
        await message.answer("Помилка з'єднання з сервером")

    await message.answer('Посилання додано, очікуйте сповіщення про нові оголошення')
