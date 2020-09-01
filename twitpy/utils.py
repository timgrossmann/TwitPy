import logging
import os
import argparse


def get_logger():
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.DEBUG)  # TO MODIFY
    fh = logging.FileHandler("logs/twitpy.log")
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    LOGGER.addHandler(fh)
    LOGGER.addHandler(ch)
    return LOGGER


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", "-d", action="store_true")
    args = parser.parse_args()
    return args
