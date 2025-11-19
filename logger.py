import logging
from datetime import datetime
import os
import sys
from os import write


def setup_logger(filename="app.log"):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    log_path = os.path.join(base_path, filename)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path, mode='w',  encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info("=" * 40)
    logging.info("Приложение запущено")

    return logging.getLogger(__name__)
