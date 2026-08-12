# conftest.py в корне reviews_bot нужен pytest, чтобы понять «отсюда начинается
# проект»: он добавит эту папку в пути импорта, и тесты смогут писать
# `from bot.ui import ...` — ровно так же, как твои модули при запуске бота.
#
# Ещё сюда кладут ФИКСТУРЫ — переиспользуемые заготовки для тестов. Любой тест
# в любом файле может попросить фикстуру, просто указав её имя в аргументах.

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db.database import Base
import db.models  # noqa: F401 — импорт регистрирует таблицы в Base.metadata


@pytest.fixture
def db_session(monkeypatch):
    """
    Даёт тесту чистую БД в оперативке вместо Postgres.

    Как пользоваться: просто добавь `db_session` в аргументы теста —
    pytest увидит имя, выполнит эту фикстуру и передаст результат.
    Каждый тест получает СВОЮ пустую базу: тесты не влияют друг на друга.
    """
    # sqlite:// (без пути к файлу) — база живёт только в памяти процесса.
    #
    # Засада, которую надо знать: in-memory SQLite своя у КАЖДОГО соединения.
    # Если не заставить SQLAlchemy держать одно соединение на весь тест,
    # create_all создаст таблицы на одном коннекте, а сессия полезет за ними
    # на другом — и получишь "no such table". StaticPool = один общий коннект.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Создаём все таблицы (reviews, responses) в этой пустой базе.
    Base.metadata.create_all(engine)

    # expire_on_commit=False — зеркалим боевой SessionLocal из db/database.py,
    # иначе тест не отражал бы реальное поведение (после commit объект отдаётся
    # наружу и читается уже без сессии).
    TestSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

    # Вот та самая подмена. crud.py достаёт SessionLocal из своего неймспейса,
    # поэтому патчим db.crud.SessionLocal — там, где им ПОЛЬЗУЮТСЯ.
    monkeypatch.setattr("db.crud.SessionLocal", TestSessionLocal)

    yield TestSessionLocal
    # После yield — teardown. Тут он не нужен: база в памяти умрёт сама,
    # а monkeypatch откатит подмену автоматически. yield просто помечает,
    # где кончается «до теста» и началось бы «после теста».
