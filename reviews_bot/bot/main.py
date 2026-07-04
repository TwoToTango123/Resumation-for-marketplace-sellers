import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from db.crud import get_pending_responses

load_dotenv()

bot = Bot(token = os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот для обработки отзывов. Я могу собирать отзывы, анализировать их и отправлять ответы.")

@dp.message(Command("pending"))
async def cmd_pending(message: Message):
    responses = get_pending_responses()
    if not responses:
        await message.answer("Все отзывы отработаны")
    else:
        for rev, resp in responses:
            text = (f"Отзыв на: {rev.product_name}\n"
            f"Оценка: {rev.rating}/5\n"
            f"{rev.text}\n"
            f"Предлагаемый ответ:\n{resp.suggested_reply}")
            await message.answer(text)

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())