import logging


def setup_logging(level=logging.INFO):
    """
    Настраивает логирование для всего приложения.

    Зовётся ОДИН раз — в точке входа (bot/main.py, pipeline.py).
    В модулях-библиотеках это вызывать НЕ надо: они только берут логгер
    через logging.getLogger(__name__) и пишут в него.

    format объясняет, что попадёт в каждую строку:
      %(asctime)s   — время
      %(levelname)s — уровень (INFO/WARNING/ERROR)
      %(name)s      — имя модуля (тот самый __name__)
      %(message)s   — сам текст
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
