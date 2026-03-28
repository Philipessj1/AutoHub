import logging
import os
import time
from datetime import datetime

# diretório dos logs
LOG_DIR = "logs"

# função para apagar logs depois de 7 dias
def cleanup_logs(days=7):
    now = time.time()

    for file in os.listdir(LOG_DIR):
        path = os.path.join(LOG_DIR, file)

        if os.path.isfile(path):
            file_age = now - os.path.getmtime(path)

            if file_age > days * 86400:
                os.remove(path)


def setup_logger(name="AutoHUB", prefix="app", log_level=logging.INFO,):
    # cria a pasta de logs se não existir
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # nome do arquivo de log com a data
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIR, f"{prefix}_{today}.log")

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # evitar duplicação
    if logger.hasHandlers():
        logger.handlers.clear()

    # formato das mensagens
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # arquivo diário
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    cleanup_logs()
    return logger