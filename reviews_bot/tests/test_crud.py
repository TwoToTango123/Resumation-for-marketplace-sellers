"""
Тесты для db/crud.py — слоя работы с БД. В отличие от чистых функций,
здесь код реально ходит в базу. Но не в Postgres: фикстура db_session
(см. conftest.py) подменяет SessionLocal на одноразовую SQLite в памяти.

Каждый тест, которому нужна база, просто добавляет db_session в аргументы —
и получает свою пустую БД. Настоящие SQLAlchemy-запросы, ноль внешних
зависимостей, миллисекунды на прогон.

Запуск (из папки reviews_bot):  python -m pytest -v
"""
from db import crud


def make_feedback(external_id="f1", rating=5, text="ок", name="Товар"):
    """Собирает словарь отзыва в формате WB — как ждёт save_feedbacks.
    Значения по умолчанию, чтобы в тесте задавать только важное."""
    return {
        "id": external_id,
        "productValuation": rating,
        "text": text,
        "productDetails": {"productName": name},
        "createdDate": "2026-06-27T10:00:00Z",
    }


def test_save_feedbacks_inserts_new(db_session):
    # Пустая база → сохраняем два разных отзыва → ждём, что оба записались.
    saved = crud.save_feedbacks([make_feedback("f1"), make_feedback("f2")])
    assert saved == 2

    # И проверяем «с другого конца»: get_new_reviews реально видит их в базе.
    reviews = crud.get_new_reviews()
    assert len(reviews) == 2
    # Новые отзывы должны иметь статус "new" (дефолт из модели).
    assert all(r.status == "new" for r in reviews)


def test_save_feedbacks_skips_duplicates(db_session):
    # Дедуп по external_id — сердце save_feedbacks. Проверяем именно его.
    crud.save_feedbacks([make_feedback("f1")])          # первый раз — записался
    saved = crud.save_feedbacks([make_feedback("f1")])  # тот же id — должен пропуститься

    assert saved == 0                        # новых не добавлено
    assert len(crud.get_new_reviews()) == 1  # в базе по-прежнему один

def test_set_status_removes_from_pending(db_session):
    crud.save_feedbacks([make_feedback("f1")])
    review = crud.get_new_reviews()[0]
    crud.save_response(review.id, {"sentiment": "positive", "suggested_reply": "ок", "needs_human": False})
    assert len(crud.get_pending_responses()) == 1
    crud.set_status(review.id, "published")
    assert len(crud.get_pending_responses()) == 0
    