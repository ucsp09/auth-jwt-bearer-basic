import logging


class Logger:
    @staticmethod
    def get_logger(name: str, level = logging.INFO):
        logger = logging.getLogger(name=name)
        logger.setLevel(level=level)
        handler = logging.StreamHandler()
        handler.setLevel(level=level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger