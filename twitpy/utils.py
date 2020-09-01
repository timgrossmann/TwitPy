import logging

def get_logger():
    logging.getLogger('selenium').setLevel(logging.WARNING)
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.DEBUG) # TO MODIFY
    fh = logging.FileHandler('etoro.log')
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    LOGGER.addHandler(fh)
    LOGGER.addHandler(ch)
    return LOGGER