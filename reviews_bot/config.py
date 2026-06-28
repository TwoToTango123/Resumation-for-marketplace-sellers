"""Настройки проекта. Значения читаются из .env."""

import os

from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# YandexGPT
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY", "")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID", "")

# Wildberries
WB_API_KEY = os.getenv("WB_API_KEY", "")

# OZON
OZON_CLIENT_ID = os.getenv("OZON_CLIENT_ID", "")
OZON_API_KEY = os.getenv("OZON_API_KEY", "")

# База данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///reviews.sqlite3")
