import os
from dotenv import load_dotenv
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.inline import get_admin_keyboard
from services.admin_se import collect_statistics
from texts.message_texts import STATS_TEXT

load_dotenv()

admin_router = Router()

ADMIN_ID = int(os.getenv('ADMIN_ID')) 

admin_router.message.filter(F.from_user.id == ADMIN_ID)

class UserStates(StatesGroup):
    waiting_for_user_data = State()

@admin_router.message(Command('admin'))
async def get_admin_menu(message: types.Message):
    await message.answer('👑 Адмін панель', reply_markup= await get_admin_keyboard())

@admin_router.callback_query(F.data == 'stats')
async def get_statistics(callback: types.CallbackQuery):
    await callback.answer()
    stats = await collect_statistics()

    await callback.message.edit_text(
        STATS_TEXT.format(
            users_count = stats.users,
            searches_count = stats.searches
        ), 
        parse_mode='HTML'
    )

@admin_router.callback_query(F.data == 'premium')
async def get_statistics(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.waiting_for_user_data)
    await callback.message.answer('✍️ Введи ID або ім\'я користувача: ')


@admin_router.message(UserStates.waiting_for_user_data)
async def give_premium(message: types.Message, state: FSMContext):
    user_data = message.text

    await state.clear()
