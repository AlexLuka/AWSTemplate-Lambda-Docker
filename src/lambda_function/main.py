import sys
import logging

from time import time, sleep


def init_logger(source, level=logging.DEBUG):
    logger_ = logging.getLogger(source)
    logger_.setLevel(level)

    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setLevel(level)

    logger_formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")
    logger_handler.setFormatter(logger_formatter)

    logger_.addHandler(logger_handler)
    return logger_


def main():
    n = 5
    t_ = time()
    for i in range(n):
        logger.info(f"Iteration {i}")
        sleep(1)
    logger.debug(f"Total execution time: {time() - t_:.10f} seconds")


if __name__ == "__main__":
    logger = init_logger(__name__)

    main()
