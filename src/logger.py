import logging
import colorlog


def setup_logging(log_file):
    """
    Sets custom logger for each part of the processing
    :param log_file: The name of the text file to store logs in it.
    :return: A logger instance
    """
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.DEBUG)

    # Create a console handler with a higher logging level (INFO)
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a file handler with the lowest logging level (DEBUG)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handlers
    log_format = "%(log_color)s%(asctime)s - %(levelname)s: %(message)s%(reset)s"
    formatter = colorlog.ColoredFormatter(log_format,
                                          datefmt="%Y-%m-%d %H:%M:%S",
                                          reset=True,
                                          log_colors={
                                              'DEBUG': 'white',
                                              'INFO': 'blue',
                                              'WARNING': 'yellow',
                                              'ERROR': 'red',
                                              'CRITICAL': 'bold_red'
                                          })

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger
