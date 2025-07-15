import asyncio
from contextlib import contextmanager

from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv

from app.db.session import SessionLocal

load_dotenv()

sst = os.getenv("BOT_TOKEN") #sst значит super secret token
bot = Bot(token = sst)

dp = Dispatcher()

@contextmanager
def get_tg_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def main():
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)

asyncio.run(main())