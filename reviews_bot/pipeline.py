from collector.wb_collector import get_unanswered_feedbacks
from db.crud import save_feedbacks, get_new_reviews, save_response, mark_processed
from ai.generator import analyze_feedback
from bot.notifier import notify_new_responses
import logging

logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("Запуск конвейера...")

    # 1. Собрать и сохранить свежие отзывы
    feedbacks = get_unanswered_feedbacks()
    saved = save_feedbacks(feedbacks)
    logger.info("Новых отзывов: %s", saved)

    # 2. Достать необработанные из БД
    new_reviews = get_new_reviews()
    logger.info("К обработке: %s", len(new_reviews))

    # 3. Каждый через AI → сохранить ответ → сменить статус
    to_notify = []
    for review in new_reviews:
        # ВНИМАНИЕ: analyze_feedback ждёт dict в формате WB,
        # а у тебя объект Review из БД.
        # Собери dict сам из полей review:
        feedback_dict = {
            "text": review.text,
            "productValuation": review.rating,
            "productDetails": {"productName": review.product_name}
        }
        result = analyze_feedback(feedback_dict)
        save_response(review.id, result)
        mark_processed(review.id)
        to_notify.append((review, result["suggested_reply"], result["needs_human"]))
        logger.info("Обработан %s: %s", review.external_id, result['sentiment'])
    
    notify_new_responses(to_notify)

    logger.info("Конвейер завершён")


if __name__ == "__main__":
    from logging_config import setup_logging
    setup_logging()
    from apscheduler.schedulers.blocking import BlockingScheduler

    run_pipeline()  # первый прогон сразу при старте

    scheduler = BlockingScheduler()
    scheduler.add_job(run_pipeline, "interval", minutes=1)  # 1 для теста
    logger.info("Планировщик запущен. Ctrl+C для остановки")
    scheduler.start()