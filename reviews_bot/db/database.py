"""Подключение к базе данных и сессии."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db() -> None:
    # TODO: создать таблицы (Base.metadata.create_all)
    raise NotImplementedError
