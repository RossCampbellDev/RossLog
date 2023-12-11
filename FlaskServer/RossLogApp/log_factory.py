import logging


def get_logger(name, filename='RossLogApp/logging/debug.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(name)s\n%(message)s')
    file_handler = logging.FileHandler(filename)
    stream_handler = logging.StreamHandler()
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger