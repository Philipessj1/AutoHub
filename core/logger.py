import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    # cria a pasta de logs se não existir
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger("AutoHUB")
    logger.setLevel(logging.DEBUG)

    # formato das mensagens
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # arquivo
    file_handler = RotatingFileHandler(
        "logs/autohub.log",
        maxBytes=1_000_000, # 1MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    # terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # evitar duplicação
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger