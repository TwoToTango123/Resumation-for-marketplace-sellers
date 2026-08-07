import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from bot.cmd_pending import router as cmd_router
import logging

logger = logging.getLogger(__name__)

load_dotenv()

bot = Bot(token = os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот для обработки отзывов. Я могу собирать отзывы, анализировать их и отправлять ответы.")

async def main():
    from logging_config import setup_logging
    setup_logging()
    logger.info("Бот запущен")
    dp.include_router(cmd_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())