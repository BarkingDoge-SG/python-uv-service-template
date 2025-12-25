import os
import logging
from logging.handlers import TimedRotatingFileHandler

from .conf_loader import ConfigLoader


class Logger:
    def __init__(self, log_name=None):
        """
        Initialize logger configuration
        :param log_name: log file name, default 'run.log'
        """
        log_config = ConfigLoader.load_module("logging")

        log_dir = log_config.get("log_dir", "./logs")
        log_level = getattr(logging, log_config.get("log_level", "INFO").upper(), logging.INFO)
        log_keeping_days = log_config.get("keeping_days", 7)
        if log_name is None:
            log_name = log_config.get("log_name", "run")

        os.makedirs(log_dir, exist_ok=True)     # create log dir

        log_path = os.path.join(log_dir, f"{log_name}.log")     # create log file
        if not os.path.exists(log_path):
            with open(log_path, 'a', encoding='utf-8'):
                pass

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # File handler
            file_handler = TimedRotatingFileHandler(
                log_path, when='D', interval=1, backupCount=log_keeping_days, encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
