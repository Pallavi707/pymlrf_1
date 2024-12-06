import logging
import os

logging_name = "pymlrf"

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger = logging.getLogger(logging_name)
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

console_handler.setFormatter(CustomFormatter())
logger.addHandler(console_handler)

try:
    # Try to fetch the environment variable 'pymlrf', and provide a fallback path if not set
    home_path = os.environ.get(logging_name, "/default/log/path")  # Fallback to a default path if not found
    
    # Check if the environment variable was not set and fallback is being used
    if home_path == "/default/log/path":
        logger.warning(f"{logging_name} environment variable not set. Using default path for logging.")
    else:
        logger.debug("Logging file path set using environment variable.")
    
    # Set up file handler for logging to file
    file_handler = logging.FileHandler(
        os.path.join(home_path, f"{logging_name}_log.txt")
    )
    file_handler.setFormatter(CustomFormatter())
    file_handler.setLevel(logging.WARNING)
    logger.addHandler(file_handler)
    logger.debug("Logging file successfully identified")

except Exception as e:
    # Catch any unexpected errors during file logging setup and log them
    logger.error(f"Error in logging setup: {e}")
