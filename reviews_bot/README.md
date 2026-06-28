# reviews_bot

Telegram-бот для сбора отзывов с Wildberries и OZON и генерации ответов через YandexGPT.

## Структура

```
reviews_bot/
├── .env                  # ключи API (в .gitignore!)
├── .gitignore
├── requirements.txt      # зависимости
├── README.md
│
├── bot/                  # Telegram-бот
│   └── main.py
│
├── collector/            # сборщик отзывов с WB/OZON
│   ├── wb_collector.py
│   └── ozon_collector.py
│
├── ai/                   # работа с YandexGPT
│   └── generator.py
│
├── db/                   # база данных
│   ├── models.py
│   └── database.py
│
└── config.py             # настройки проекта
```

## Запуск

```bash
pip install -r requirements.txt
cp .env.example .env   # заполнить ключи
python -m bot.main
```
