from datetime import datetime, timezone, timedelta
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from texts.message_texts import COMMAND_START, SEARCHES_LIMIT, \
NEW_SEARCHES, HELP_TEXT, MY_SEARCHS_TEXT, ADD_SEARCHES, PREMIUM_TEXT
from services.advert_se import add_new_search_link, get_my_searches, \
change_status_in_search, clean_search
from models.tables_models import User
from repositories.users import create_user
from core.exceptions import LimitExceeded
from keyboards.menu import keyboard
from keyboards.inline import get_search_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    await create_user(
        User(
            id=user_id, 
            username=username, 
            max_searches=3,
            premium_expires_at=datetime.now(timezone.utc) + timedelta(days=3)
        )
    )

    await message.answer(
        COMMAND_START.format(username=username), 
        reply_markup=keyboard
    )

@router.message(F.text.contains('https://www.olx.ua'))
async def new_search_link(message: types.Message):
    link = message.text
    user_id = message.from_user.id
    try:
        await add_new_search_link(link, user_id)
        await message.answer(NEW_SEARCHES, parse_mode='HTML')
    except LimitExceeded:
        await message.answer(SEARCHES_LIMIT, parse_mode='HTML')

@router.message(F.text == 'ℹ️ Допомога')
async def help_info(message: types.Message):
    await message.answer(HELP_TEXT, parse_mode='HTML')

@router.message(F.text == '🔍 Мої пошуки')
async def my_searches(message: types.Message):
    user_id = message.from_user.id
    searches = await get_my_searches(user_id)
    for search in searches:
        answer_text = MY_SEARCHS_TEXT.format(
            url = search.search_link,
            created_at = search.created_at.strftime('%d.%m'),
            status = '🟢 Активно' if search.is_active else '🔴 Не активно'
        )
        await message.answer(
            answer_text, 
            reply_markup=get_search_keyboard(search.is_active, search.id)
        )

@router.callback_query(F.data.startswith('status'))
async def process_quality_choice(callback: types.CallbackQuery):
    await callback.answer()
    
    user_id = callback.from_user.id
    search_id = callback.data.split(':')[1]
    
    try:
        search = await change_status_in_search(int(search_id), user_id)
        edited_text = MY_SEARCHS_TEXT.format(
            url = search.search_link,
            created_at = search.created_at.strftime('%d.%m'),
            status = '🟢 Активно' if search.is_active else '🔴 Не активно'
        )
        await callback.message.edit_text(
            edited_text, 
            reply_markup=get_search_keyboard(search.is_active, search.id)
        )
    except LimitExceeded:
        await callback.message.edit_text(SEARCHES_LIMIT, parse_mode='HTML')

@router.callback_query(F.data.startswith('delete'))
async def delete_message(callback: types.CallbackQuery):
    search_id = callback.data.split(':')[-1]
    await clean_search(int(search_id))
    await callback.message.delete()

@router.message(F.text == '➕ Додати')
async def help_info(message: types.Message):
    await message.answer(ADD_SEARCHES, parse_mode='HTML')

@router.message(F.text == '⭐ Преміум')
async def help_info(message: types.Message):
    await message.answer(PREMIUM_TEXT, parse_mode='HTML')