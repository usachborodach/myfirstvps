import os
from datetime import datetime
import logging
os.chdir(os.path.dirname(__file__))
current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler('debug.log')]
    )
    info_handler = logging.FileHandler('info.log')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    root_logger = logging.getLogger()
    root_logger.addHandler(info_handler)

def log_info(message):
    logging.info(message)

def log_debug(message):
    logging.debug(message)

def log_error(message):
    logging.error(message)

def log_warning(message):
    logging.warning(message)

setup_logging()