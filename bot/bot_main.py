import asyncio

from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv

load_dotenv()

sst = os.getenv("BOT_TOKEN") #sst значит super secret token
bot = Bot(token = sst)

dp = Dispatcher()

async def main():
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)

asyncio.run(main())