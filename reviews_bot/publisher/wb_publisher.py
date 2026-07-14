def publish_reply(external_id: str, text: str) -> bool:
    """
    Публикует ответ на отзыв в WB.
    Пока mock: печатает в консоль, реального запроса нет.
    Возвращает True при успехе, False при ошибке.

    ВАЖНО: функция синхронная и блокирующая - позже здесь будет
    requests.post() к API WB. Вызывать ее из бота нужно через
    asyncio.to_thread(), иначе повесишь event loop.
    """
    try:
        print(f"Публикую ответ на отзыв {external_id}: {text}")
        return True
    except Exception as e:
        print(f"Ошибка публикации: {e}")
        return False