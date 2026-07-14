from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
from db.crud import get_pending_responses, set_status, get_publish_data
from publisher.wb_publisher import publish_reply
from bot.ui import format_review_card, moderation_keyboard
import asyncio

router = Router()

@router.message(Command("pending"))
async def cmd_pending(message):
    responses = get_pending_responses()
    if not responses:
        await message.answer("Все отзывы отработаны")
    else:
        for review, response in responses:
            text = format_review_card(review, response.suggested_reply, response.needs_human)
            keyboard = moderation_keyboard(review.id)
            await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data.startswith("publish:"))
async def on_publish(callback: CallbackQuery):
    review_id = int(callback.data.split(":")[1])
    data = get_publish_data(review_id)
    if data is None:
        await callback.message.edit_text("Ошибка: не удалось получить данные для публикации")
        await callback.answer()
        return
    else:
        external_id, suggested_reply = data
    await callback.answer()
    set_status(review_id, "publishing")
    ok = await asyncio.to_thread(publish_reply, external_id, suggested_reply)
    if ok:
        set_status(review_id, "published")
        await callback.message.edit_text("✅Опубликовано на WB")
    else:
        set_status(review_id, "failed")
        await callback.message.edit_text("❌Не удалось опубликовать на WB")


@router.callback_query(F.data.startswith("skip:"))
async def on_skip(callback: CallbackQuery):
    review_id = int(callback.data.split(":")[1])
    set_status(review_id, "skipped")
    await callback.message.edit_text("Ответ пропущен")
    await callback.answer()