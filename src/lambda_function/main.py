import sys
import logging
import numpy as np

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


def handler(input_data, lambda_context, *args, **kwargs):
    """
        Note, this name is used in a CMD command in Dockerfile.

    :param input_data:
    :param lambda_context:
    :param args:
    :param kwargs:
    :return:
    """
    logger = init_logger(__name__)

    n = 10
    t_ = time()
    for i in range(n):
        logger.info(f"Iteration {i}: random number is {np.random.rand()}")
        sleep(1)
    logger.debug(f"Total execution time: {time() - t_:.10f} seconds")


if __name__ == "__main__":
    handler(None, None, None, None)
