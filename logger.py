import logging


file_log = logging.FileHandler("Log.log")
console_out = logging.StreamHandler()

logging.basicConfig(
    handlers=(file_log, console_out),
    format="[%(asctime)s | %(levelname)s]: %(message)s",
    datefmt="%m.%d.%Y %H:%M:%S",
    level=logging.INFO,
)

root_logger = logging.getLogger(__name__)
root_logger.setLevel(logging.DEBUG)
