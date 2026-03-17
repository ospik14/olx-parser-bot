from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_search_keyboard(is_active: bool, search_id: int):

    btn_change_status = InlineKeyboardButton(
        text="🟢 Активувати" if not is_active else '🔴 Деактивувати', 
        callback_data=f"status:{search_id}",
    )
    btn_delete = InlineKeyboardButton(
        text='❌ Видалити',
        callback_data=f"delete:{search_id}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_change_status],
            [btn_delete]
        ]
    )
    return keyboard

async def get_admin_keyboard():

    btn_stats = InlineKeyboardButton(
        text='📊 Статистика',
        callback_data='stats'
    )
    btn_give_premium = InlineKeyboardButton(
        text='⭐ Надати преміум',
        callback_data='premium'
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_stats], 
            [btn_give_premium]
        ]
    )

    return keyboard