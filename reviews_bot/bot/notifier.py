import asyncio, os
from aiogram import Bot
from dotenv import load_dotenv
from bot.ui import format_review_card, moderation_keyboard
import logging

logger = logging.getLogger(__name__)

load_dotenv()

async def _send_all(items: list) -> None:
    """items — список пар (review, response)."""
    bot = Bot(token = os.getenv("TELEGRAM_BOT_TOKEN"))
    chat_id = os.getenv("SELLER_CHAT_ID")
    try:
        for review, suggested_reply, needs_human in items:
            try:
                text = format_review_card(review, suggested_reply, needs_human)
                keyboard = moderation_keyboard(review.id)
                await bot.send_message(chat_id = chat_id, text = text, reply_markup = keyboard)
            except Exception as e:
                logger.error("Ошибка отправки отзыва %s: %s", review.id, e)
    finally:
        await bot.session.close()

def notify_new_responses(items: list) -> None:
    """Синхронная обертка - ее зовет pipeline."""
    if not items:
        logger.info("Нет новых ответов для отправки")
        return
    asyncio.run(_send_all(items))
