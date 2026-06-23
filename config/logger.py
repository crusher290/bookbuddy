import logging
from datetime import datetime
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bookbuddy.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_info(message: str) -> None:
    logger.info(message)


def log_error(message: str) -> None:

    logger.error(message)


def log_warning(message: str) -> None:
    logger.warning(message)


def log_debug(message: str) -> None:
    logger.debug(message)


def log_book_action(action: str, book_title: str) -> None:

    log_info(f"[BOOK ACTION] {action}: {book_title}")


def log_file_action(action: str, filename: str) -> None:
    log_info(f"[FILE ACTION] {action}: {filename}")


def log_error_with_context(error: Exception, context: Optional[str] = None) -> None:
    if context:
        log_error(f"[ERROR] {context}: {str(error)}")
    else:
        log_error(f"[ERROR] {str(error)}")