
import time
import logging
import functools
import traceback

logger = logging.getLogger("game")
logger.setLevel(logging.INFO)
logger.propagate = False  

file_handler = logging.FileHandler(
    "game.log",
    mode="a",
    encoding="utf-8"
)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

logger.addHandler(file_handler)

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = int(time.time() - start)
        mins, secs = divmod(elapsed, 60)

        message = f"Время игры: {mins} мин {secs} сек"
        print(message)
        logger.info(message)

        return result
    return wrapper

def log_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error("{func.name}\n{traceback.format_exc()}")
            raise
    return wrapper