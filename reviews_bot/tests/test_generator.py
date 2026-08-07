"""
Тесты для ai/generator.parse_ai_response — чистой функции, которую мы
специально вынесли из analyze_feedback. Она разбирает СЫРОЙ текст ответа
YandexGPT в dict. Никакой сети: подаём строку, проверяем результат.

Именно ради этого делался рефакторинг «раздели I/O и логику»: поход в
нейросеть остался в analyze_feedback (его тестировать дорого и ненадёжно),
а весь разбор — здесь, и он проверяется мгновенно и бесплатно.

Импорт `from ai.generator import parse_ai_response` безопасен: на уровне
модуля есть только load_dotenv() и os.getenv() — в сеть при импорте
ничего не ходит.

Запуск (из папки reviews_bot):  python -m pytest -v
"""
import requests
from ai.generator import parse_ai_response, analyze_feedback

class FakeResponse:
    """Подделка под объект, который возвращает requests.post.
    Реализует ровно те методы, что вызывает analyze_feedback: .json() и
    .raise_for_status(). Если передать error — raise_for_status его бросит
    (имитация ответа 4xx/5xx)."""
    def __init__(self, text="", error=None):
        self._text = text
        self._error = error

    def json(self):
        return {"result": {"alternatives": [{"message": {"text": self._text}}]}}

    def raise_for_status(self):
        # Настоящий requests: на 2xx молчит, на 4xx/5xx кидает HTTPError.
        if self._error is not None:
            raise self._error

# --- Ветка 1: чистый JSON --------------------------------------------------
# Самый обычный случай — модель вернула ровно JSON, без обёрток.

def test_parses_clean_json():
    raw = '{"sentiment": "positive", "suggested_reply": "Спасибо!", "needs_human": false}'
    result = parse_ai_response(raw)

    # Проверяем, что каждое поле распарсилось в нужный тип и значение.
    # false в JSON → False в Python, это тоже стоит зафиксировать.
    assert result["sentiment"] == "positive"
    assert result["suggested_reply"] == "Спасибо!"
    assert result["needs_human"] is False


# --- Ветка 2: JSON в markdown-обёртке ```json ... ``` ----------------------
# Модели часто оборачивают ответ в тройные кавычки, будто это код.
# Твоя функция должна снять обёртку и префикс "json" и всё равно распарсить.
# Ровно эту чистку мы чинили по отступам — вот тест, который её сторожит.

def test_parses_json_wrapped_in_markdown_fence():
    raw = '```json\n{"sentiment": "negative", "suggested_reply": "Извините", "needs_human": true}\n```'
    result = parse_ai_response(raw)

    assert result["sentiment"] == "negative"
    assert result["suggested_reply"] == "Извините"
    assert result["needs_human"] is True


# --- Ветка 2б: обёртка ``` БЕЗ префикса json -------------------------------
# Тот самый случай, ради которого важен был правильный отступ strip():
# обёртка есть, а слова "json" нет. Функция обязана справиться и тут.

def test_parses_json_wrapped_without_json_prefix():
    raw = '```\n{"sentiment": "neutral", "suggested_reply": "ок", "needs_human": false}\n```'
    result = parse_ai_response(raw)

    assert result["sentiment"] == "neutral"
    assert result["needs_human"] is False


# --- Ветка 3: битый текст → заглушка --------------------------------------
# Модель может ответить не-JSON (заговорить словами, оборваться на полуслове).
# Тогда json.loads падает, и функция ОБЯЗАНА вернуть безопасную заглушку,
# а не уронить весь пайплайн. Это «предохранитель» системы.

def test_broken_text_returns_safe_fallback():
    raw = "Извините, я не смог обработать этот отзыв"
    result = parse_ai_response(raw)

    # Заглушка: тональность нейтральная, needs_human=True (зови человека),
    # а сырой текст кладётся в suggested_reply, чтобы он не потерялся.
    assert result["sentiment"] == "neutral"
    assert result["needs_human"] is True
    assert result["suggested_reply"] == raw


def test_fallback_has_all_three_keys():
    """Даже на мусоре результат должен содержать все три ключа —
    иначе код ниже по пайплайну (save_response) упадёт на result['sentiment']."""
    result = parse_ai_response("не json вовсе")
    assert set(result.keys()) == {"sentiment", "suggested_reply", "needs_human"}

def test_analyze_feedback_parses_model_reply(monkeypatch):
    fake_json = '{"sentiment": "positive", "suggested_reply": "Спасибо!", "needs_human": false}'
    def fake_post(*args, **kwargs):
        return FakeResponse(fake_json)
    monkeypatch.setattr("ai.generator.requests.post", fake_post)
    feedback = {
        "productDetails": {"productName": "Товар"},
        "productValuation": 5,
        "text": "Отлично!"
    }
    result = analyze_feedback(feedback)
    assert result['sentiment'] == "positive"
    assert result['needs_human'] is False

def test_analyze_feedback_falls_back_on_garbage(monkeypatch):
    def fake_post(*args, **kwargs):
        return FakeResponse("не json вовсе")
    monkeypatch.setattr("ai.generator.requests.post", fake_post)
    feedback = {
        "productDetails": {"productName": "Товар"},
        "productValuation": 5,
        "text": "Отлично!"
    }
    result = analyze_feedback(feedback)
    assert result['sentiment'] == "neutral"
    assert result['needs_human'] is True
    assert result['suggested_reply'] == "не json вовсе"

def test_analyze_feedback_falls_back_on_http_error(monkeypatch):
    """YandexGPT вернул 4xx/5xx → raise_for_status кинет HTTPError →
    analyze_feedback ловит и отдаёт безопасную заглушку, НЕ падает."""
    # FakeResponse с error: её raise_for_status() бросит HTTPError.
    def fake_post(*args, **kwargs):
        return FakeResponse(error=requests.exceptions.HTTPError("429 Too Many Requests"))
    monkeypatch.setattr("ai.generator.requests.post", fake_post)
    feedback = {
        "productDetails": {"productName": "Товар"},
        "productValuation": 5,
        "text": "Отлично!"
    }
    result = analyze_feedback(feedback)
    # Главное: не исключение, а заглушка с needs_human=True (отзыв → к человеку).
    assert result['needs_human'] is True
    assert result['sentiment'] == "neutral"

def test_analyze_feedback_falls_back_on_network_error(monkeypatch):
    """Сеть упала → requests.post кинет RequestException →
    analyze_feedback ловит и отдаёт безопасную заглушку, НЕ падает."""
    def fake_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Сеть недоступна")
    monkeypatch.setattr("ai.generator.requests.post", fake_post)
    feedback = {
        "productDetails": {"productName": "Товар"},
        "productValuation": 5,
        "text": "Отлично!"
    }
    result = analyze_feedback(feedback)
    assert result['needs_human'] is True
    assert result['sentiment'] == "neutral"