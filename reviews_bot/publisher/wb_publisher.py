import logging

logger = logging.getLogger(__name__)


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
        # %s-аргументы, а не f-строка: logging подставит их ЛЕНИВО — только
        # если этот уровень включён. Идиома логирования.
        logger.info("Публикую ответ на отзыв %s: %s", external_id, text)
        return True
    except Exception as e:
        # .error — уровень для сбоев. (Есть ещё logger.exception — то же самое,
        # но добавит трейсбек; удобно внутри except.)
        logger.error("Ошибка публикации отзыва %s: %s", external_id, e)
        return False