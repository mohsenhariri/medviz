import logging
from os import getenv
from pathlib import Path

from .custom_type import PathType
from .utility import now


def logger_init(file_name: str):
    log_root = getenv("PATH_LOGS")

    path_logs: PathType = Path(log_root) if log_root != None else Path("./logs")

    if not path_logs.exists():
        path_logs.mkdir(parents=True)

    current_time = now()

    logging.basicConfig(
        filename=rf"{path_logs}/{file_name}_{current_time}.log",
        format="%(asctime)s %(message)s",
        encoding="utf-8",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(file_name)
    logger.info("Start.")

    return logger
