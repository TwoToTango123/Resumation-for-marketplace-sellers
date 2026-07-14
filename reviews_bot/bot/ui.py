from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def format_review_card(review, suggested_reply: str, needs_human: bool) -> str:
    """
    Текст карточки отзыва. Один вид и для /pending, и для пуша.
    """
    text = (f"Отзыв на: {review.product_name}\n"
            f"Оценка: {review.rating}/5\n"
            f"{review.text}\n"
            f"Предлагаемый ответ:\n{suggested_reply}")
    if needs_human:
        text += "\n⚠️ Требует внимания"
    return text

def moderation_keyboard(review_id: int) -> InlineKeyboardMarkup:
    """Две кнопки: опубликовать/пропустить"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(text="Опубликовать", callback_data=f"publish:{review_id}"),
        InlineKeyboardButton(text="Пропустить", callback_data=f"skip:{review_id}")
        ]
    ])
    return keyboard
