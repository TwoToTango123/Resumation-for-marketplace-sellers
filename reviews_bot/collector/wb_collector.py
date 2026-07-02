from collector.mock_data import MOCK_FEEDBACKS
from datetime import datetime

def get_unanswered_feedbacks() -> list[dict]:
    """
    Возвращает отзывы без ответа.
    Сейчас работает на mock-данных.
    Когда появится токен WB — заменим на реальный API.
    """
    result = [feedback for feedback in MOCK_FEEDBACKS if feedback["answer"] is None]
    return result

def print_feedback(feedback: dict) -> None:
    """Красиво печатает один отзыв в консоль"""
    print(f'ID: {feedback['id']}')
    print(f'Name: {feedback['productDetails']['productName']}')
    print(f'Rating: {'⭐' * (feedback['productValuation'])}')
    date = datetime.fromisoformat(feedback['createdDate'].replace('Z', '+00:00'))
    formatted = date.strftime("%d.%m.%Y")
    print(f'Date: {formatted}')
    print(f'Text: {feedback['text']}')
    print('-' * 40)

def main():
    from db.crud import save_feedbacks

    feedbacks = get_unanswered_feedbacks()
    print(f"Найдено отзывов без ответа: {len(feedbacks)}\n")

    saved = save_feedbacks(feedbacks)
    print(f"Сохранено новых отзывов: {saved}")

    for feedback in feedbacks:
        print_feedback(feedback)
    
if __name__ == "__main__":
    main()