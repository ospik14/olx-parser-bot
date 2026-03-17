import asyncio
import logging
from aiogram import Bot
from loader import bot, dp
from handlers import bot_commands, admin_commands
from services.main_process import pars_loop, check_premium

logging.basicConfig(level=logging.INFO)


async def on_startup(bot: Bot):
    asyncio.create_task(pars_loop())
    asyncio.create_task(check_premium())

async def main():
    dp.include_router(router=bot_commands.router)
    dp.include_router(router=admin_commands.admin_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())