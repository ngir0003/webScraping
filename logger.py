#logger.py
import logging
import os

def setup_logger(name, log_file='movies_series.log', level=logging.INFO):
    os.makedirs('logs', exist_ok=True)
    handler = logging.FileHandler(f'logs/{log_file}')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

logger = setup_logger('movie_scraper')