import logging


class ColoredFormatter(logging.Formatter):
    """Custom formatter class to add colors to log messages based on level"""

    def __init__(self, fmt):
        super().__init__()
        self.fmtstr = fmt
        self.colors = {
            logging.DEBUG: '\033[94m',  # Light blue
            logging.INFO: '\033[92m',   # Light green
            logging.WARNING: '\033[93m',  # Yellow
            logging.ERROR: '\033[31;2m',   # Bold Red
            logging.CRITICAL: '\033[91m',  # Red
        }
        self.reset = '\033[0m'  # Reset color

    def format(self, record):
        log_fmt = self.colors.get(record.levelno) + self.fmtstr + self.reset
        return logging.Formatter(log_fmt).format(record)


def setup_logging():
    # Create logger
    logger = logging.getLogger("__main__")
    # logger.file_name = '/var/log/road/app.log'

    # Set logger level (optional, defaults to WARNING)
    logger.setLevel(logging.DEBUG)

    # Create console handler
    console_handler = logging.StreamHandler()

    # Create colored formatter
    formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set formatter on handler
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    logger.debug("Logger setup complete")
