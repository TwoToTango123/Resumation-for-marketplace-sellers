# Mock-данные реальной структуры WB API
# Когда появится токен — этот файл просто удалим

MOCK_FEEDBACKS = [
    {
        "id": "feed_001",
        "text": "Отличные кроссовки! Размер совпал с таблицей, "
                "материал качественный. Доставка быстрая. Рекомендую!",
        "productValuation": 5,
        "createdDate": "2026-06-27T10:00:00Z",
        "productDetails": {
            "nmId": 12345678,
            "productName": "Кроссовки мужские беговые"
        },
        "answer": None  # None = без ответа = наш клиент
    },
    {
        "id": "feed_002",
        "text": "Товар не соответствует описанию. "
                "На фото цвет синий, пришёл серый. "
                "Очень расстроена, ждала месяц.",
        "productValuation": 2,
        "createdDate": "2026-06-27T11:30:00Z",
        "productDetails": {
            "nmId": 12345678,
            "productName": "Кроссовки мужские беговые"
        },
        "answer": None
    },
    {
        "id": "feed_003",
        "text": "Нормально, ничего особенного. "
                "За эту цену сойдёт.",
        "productValuation": 3,
        "createdDate": "2026-06-27T12:00:00Z",
        "productDetails": {
            "nmId": 87654321,
            "productName": "Футболка хлопок базовая"
        },
        "answer": None
    },
    {
        "id": "feed_004",
        "text": "Брак! Разошёлся шов на второй день носки. "
                "Качество ужасное, деньги на ветер. "
                "Требую возврат!",
        "productValuation": 1,
        "createdDate": "2026-06-27T13:00:00Z",
        "productDetails": {
            "nmId": 87654321,
            "productName": "Футболка хлопок базовая"
        },
        "answer": None
    },
    {
        "id": "feed_005",
        "text": "Уже третий раз заказываю у этого продавца. "
                "Всегда всё чётко: качество, упаковка, сроки.",
        "productValuation": 5,
        "createdDate": "2026-06-27T14:00:00Z",
        "productDetails": {
            "nmId": 11111111,
            "productName": "Носки спортивные набор 5 пар"
        },
        "answer": None
    },
    {
        "id": "feed_006",
        "text": "Пришла не та расцветка что заказывал. "
                "Но качество самого товара хорошее, "
                "оставлю себе.",
        "productValuation": 3,
        "createdDate": "2026-06-27T15:00:00Z",
        "productDetails": {
            "nmId": 11111111,
            "productName": "Носки спортивные набор 5 пар"
        },
        "answer": None
    },
]
