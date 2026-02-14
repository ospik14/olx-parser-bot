import asyncio
import logging
from aiogram import Bot
from loader import bot, dp
from handlers import bot_commands
from services.main_process import pars_loop

logging.basicConfig(level=logging.INFO)


async def on_startup(bot: Bot):
    asyncio.create_task(pars_loop())

async def main():
    dp.include_router(router=bot_commands.router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())