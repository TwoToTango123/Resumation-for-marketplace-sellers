from db.database import SessionLocal
from db.models import Review
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
