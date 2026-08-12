from db.database import SessionLocal
from db.models import Review, Response, ResponseStatus, ReviewStatus, Seller
from datetime import datetime

def save_feedbacks(feedbacks: list[dict]) -> int:
    """
    Сохраняет отзывы в ДБ.
    Пропускает дубли (проверка по external_id).
    Возвращает количество новых.
    """
    session = SessionLocal()
    saved_count = 0

    try:
        for feedback in feedbacks:
            exists = session.query(Review).filter(
                Review.external_id == feedback["id"]
            ).first()
            if exists:
                continue
            else:
                review = Review(
                external_id=feedback["id"],
                marketplace="wb",
                product_name=feedback["productDetails"]["productName"],   # достань из вложенного dict
                rating=feedback["productValuation"],
                text=feedback["text"],
                created_at=datetime.fromisoformat(feedback["createdDate"].replace("Z", "+00:00"))
                )
                session.add(review)
                saved_count += 1
        session.commit()
        return saved_count
    finally:
        session.close()

def get_new_reviews() -> list[Review]:
    """
    Возвращает все отзывы со status = 'new'
    """
    session = SessionLocal()
    try:
        new_reviews = session.query(Review).filter(Review.status == ReviewStatus.NEW).all()
        return new_reviews
    finally:
        session.close()

def save_response(review_id: int, ai_result: dict) -> None:
    """
    Сохраняет ответ AI в таблицу responses
    """
    session = SessionLocal()
    try:
        response = Response(
            review_id = review_id,
            sentiment = ai_result["sentiment"],
            suggested_reply = ai_result["suggested_reply"],
            needs_human = ai_result["needs_human"]
        )
        session.add(response)
        session.commit()
    finally:
        session.close()

def mark_processed(review_id: int) -> None:
    """
    Меняет статус отзыва на 'processed'
    """
    session = SessionLocal()
    try:
        review = session.query(Review).filter(Review.id == review_id).first()
        if review:
            review.status = ReviewStatus.PROCESSED
            session.commit()
    finally:
        session.close()

def get_pending_responses() -> list:
    """
    Возвращает пары (Review, Response) где response.status == 'pending'.
    """
    session = SessionLocal()
    try:
        results = (
            session.query(Review, Response).join(Response, Response.review_id == Review.id).filter(Response.status == ResponseStatus.PENDING).all()
        )
        return results
    finally:
        session.close()

def set_status(review_id: int, status: ResponseStatus) -> None:
    """
    Универсальная замена mark_published - ставит любой статус.
    """
    session = SessionLocal()
    try:
        response = session.query(Response).filter(Response.review_id == review_id).first()
        if response:
            response.status = status
            session.commit()
    finally:
        session.close()

def get_publish_data(review_id: int) -> tuple[str, str] | None:
    """
    Возвращает (external_id, suggested_reply) для отзыва.
    Если данных нет - возвращает None.
    Одним запросом с join - не два обращения к БД.
    """
    session = SessionLocal()
    try:
        result = (
            session.query(Review.external_id, Response.suggested_reply)
            .join(Response, Response.review_id == Review.id)
            .filter(Review.id == review_id)
            .first()
        )
        if result:
            return (result.external_id, result.suggested_reply)
        else:
            return None
    finally:
        session.close()

def get_or_create_seller(chat_id: str, brand_name: str) -> tuple[Seller, bool]:
    """
    Ищет селлера по chat_id.
    Есть  → возвращает (seller, False).
    Нет   → создаёт с brand_name, возвращает (seller, True).
    """
    session = SessionLocal()
    try:
        seller = session.query(Seller).filter(Seller.chat_id == chat_id).first()
        if seller:
            return seller, False
        else:
            new_seller = Seller(chat_id=chat_id, brand_name=brand_name)
            session.add(new_seller)
            session.commit()
            return new_seller, True
    finally:
        session.close()
    