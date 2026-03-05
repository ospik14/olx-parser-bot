from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_search_keyboard(is_active: bool):

    btn_change_status = InlineKeyboardButton(
        text="🟢 Активувати" if not is_active else '🔴 Деактивувати', 
        callback_data="status"
    )
    btn_delete = InlineKeyboardButton(
        text='❌ Видалити',
        callback_data="delete"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_change_status],
            [btn_delete]
        ]
    )
    return keyboard