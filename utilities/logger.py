
import logging
import inspect
import os
from time import gmtime, strftime


class Logger:
    logger = None

    def get_logger(self):
        return Logger.logger

    def set_up(self, target):

        Logger.logger = logging.getLogger('xposd')
        Logger.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(f'scan-{target}.out')
        stream_handler = logging.StreamHandler()

        file_handler.setLevel(logging.DEBUG)
        stream_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s -[%(levelname)s]- %(message)s','%H:%M:%S')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        Logger.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def info(self, msg):
        logger = self.get_logger()
        logger.info(msg)

    def error(self, msg):
        logger = self.get_logger()
        logger.error(msg)

    def debug(self, msg):
        logger = self.get_logger()
        logger.debug(msg)

    def warning(self, msg):
        logger = self.get_logger()
        logger.warning(msg)

