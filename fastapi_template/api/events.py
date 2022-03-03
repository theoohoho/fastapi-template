from loguru import logger


def startup_app_handler():
    logger.info("Start startup handler")


def shutdown_app_handler():
    logger.info("Start shutdown handler")
