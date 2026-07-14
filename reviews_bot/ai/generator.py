import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

def analyze_feedback(feedback: dict) -> dict:
    """
    Принимает отзыв, возыращает dict с ключами:
    - sentiment: positive / negative / neutral
    - suggested_reply: готовый ответ
    - needs_human: True / False
    """

    system_prompt = """Ты - помощник по анализу отзывов. 
    Отвечай на отзывы вежливо и по-человечески. 
    Твоя задача определить тональность отзыва 
    (положительная, отрицательная или нейтральная), 
    а также предложить готовый ответ на отзыв. 
    Если отзыв содержит оскорбления, угрозы, нецензурную лексику, 
    требование воврата или денег, жалобы о вреде здоровью,
    или если отзыв явно негативный и требует вмешательства человека,
    в поле needs_human нужно поставить True. В противном случае, 
    в поле needs_human нужно поставить False. 
    Ответ должен быть в формате JSON с ключами: 
    sentiment, suggested_reply, needs_human. 
    Пример ответа: {"sentiment": "positive", "suggested_reply": 
    "Спасибо за ваш отзыв!", "needs_human": false}"""

    user_prompt = f"""Товар: {feedback['productDetails']['productName']}
    Оценка: {feedback['productValuation']} из 5
    Отзыв: {feedback['text']}"""

    response = requests.post(
        YANDEX_API_URL,
        headers = {
            "Authorization": f"Api-Key {YANDEX_API_KEY}",
            "Content-Type": "application/json"
        },
        json = {
            "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt/latest",
            "completionOptions": {
                "temperature": 0.3,
                "maxTokens": 500
            },
            "messages": [
                {"role": "system", "text": system_prompt},
                {"role": "user", "text": user_prompt}
            ]
        }
    )

    raw_text = response.json()["result"]["alternatives"][0]["message"]["text"]

    try:
        raw_text = raw_text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
            raw_text = raw_text.strip()
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        # JSON не распарсился — возвращаем заглушку
        # чтобы программа не упала
        result = {
            "sentiment": "neutral",
            "suggested_reply": raw_text,  # отдаём сырой текст
            "needs_human": True  # помечаем что нужен человек
        }

    return result

def main():
    from collector.mock_data import MOCK_FEEDBACKS

    for feedback in MOCK_FEEDBACKS:
        print(f"Анализирую {feedback["id"]}")
        result = analyze_feedback(feedback)
        print(f"Тональность: {result['sentiment']}")
        print(f"Нужен человек: {result['needs_human']}")
        print(f"Ответ: {result["suggested_reply"]}")
        print("*" * 40)

if __name__ == "__main__":
    main()