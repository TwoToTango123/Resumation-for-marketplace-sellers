"""
Тесты для bot/ui.py — чистых функций, которые собирают карточку отзыва
и клавиатуру. Начинаем именно с них, потому что они НЕ ходят в БД, в сеть
и в Telegram: подал на вход данные — получил результат. Такие функции
тестировать проще всего, поэтому это идеальный первый шаг.

Как запустить (из папки reviews_bot):
    python -m pytest
или подробнее:
    python -m pytest -v
"""
from types import SimpleNamespace

from bot.ui import format_review_card, moderation_keyboard


# --- Вспомогательное -------------------------------------------------------
# format_review_card ждёт объект review с полями .product_name, .rating, .text.
# Настоящий Review из БД тащить в тест не нужно (это подключение к Postgres).
# SimpleNamespace — это «объект-заглушка»: даёшь ему поля, он их отдаёт.
# fake_review().product_name вернёт "Кроссовки". Ровно то, что нужно функции.
def fake_review():
    return SimpleNamespace(
        product_name="Кроссовки",
        rating=2,
        text="Отличный товар",
    )


# --- Тесты format_review_card ---------------------------------------------
# Правило именования: файл test_*.py, функции test_*. Так pytest их находит сам.

def test_card_contains_review_fields():
    """В карточке должны быть все данные отзыва и предложенный ответ."""
    card = format_review_card(fake_review(), suggested_reply="Спасибо!", needs_human=False)

    # assert — сердце теста. Если условие ложно, тест падает и показывает, что не так.
    # Проверяем, что каждый кусок данных реально попал в текст.
    assert "Кроссовки" in card
    assert "2/5" in card
    assert "Отличный товар" in card
    assert "Спасибо!" in card


def test_card_shows_warning_when_needs_human():
    """needs_human=True → в карточке есть пометка про внимание."""
    card = format_review_card(fake_review(), suggested_reply="Ответ", needs_human=True)
    assert "Требует внимания" in card


def test_card_hides_warning_when_not_needs_human():
    """needs_human=False → пометки быть НЕ должно.
    Это «негативный» тест: проверяем не только что что-то появляется,
    но и что лишнее НЕ появляется. Про такие часто забывают, а зря."""
    card = format_review_card(fake_review(), suggested_reply="Ответ", needs_human=False)
    assert "Требует внимания" not in card


# --- Тесты moderation_keyboard --------------------------------------------
# Вот ради этого теста во многом всё и затевалось: он фиксирует ФОРМАТ
# callback_data. Именно его ты однажды случайно сломал (publish: → publish_)
# и уронил рабочий /pending. Теперь такая регрессия упадёт здесь за полсекунды.

def test_keyboard_callback_data_format():
    """Кнопки должны нести callback_data строго вида 'publish:<id>' и 'skip:<id>'.
    Хендлеры в cmd_pending.py режут строку по ':' — формат обязан совпадать."""
    kb = moderation_keyboard(review_id=42)

    # inline_keyboard — это список рядов, каждый ряд — список кнопок.
    # У нас один ряд с двумя кнопками: [[кнопка_publish, кнопка_skip]].
    first_row = kb.inline_keyboard[0]
    publish_btn, skip_btn = first_row

    assert publish_btn.callback_data == "publish:42"
    assert skip_btn.callback_data == "skip:42"

def test_rating_format_is_correct():
    """Рейтинг должен быть в формате 'X/5'."""
    card = format_review_card(fake_review(), suggested_reply="Ответ", needs_human=False)
    assert "2/5" in card

def test_keyboard_has_two_buttons_in_one_row():
    """Клавиатура должна содержать две кнопки в одном ряду."""
    keyboard = moderation_keyboard(review_id=1)
    assert len(keyboard.inline_keyboard) == 1
    assert len(keyboard.inline_keyboard[0]) == 2
