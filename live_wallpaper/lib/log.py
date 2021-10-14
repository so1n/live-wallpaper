import logging
import pathlib


def init_logging(log_level: str) -> None:
    logging.basicConfig(
        format="%(levelname)s [%(asctime)s %(name)s:%(lineno)d] %(message)s",
        datefmt="%y%m%d %H:%M:%S",
        level=getattr(logging, log_level.upper(), "INFO"),
    )


def init_file_logging(path_str: str, log_level: str) -> None:
    log_filename: str = path_str + "/live-wallpaper.log"
    log_path: pathlib.Path = pathlib.Path(path_str)
    if not log_path.exists():
        log_path.mkdir(parents=True)
    logging.basicConfig(
        filename=log_filename,
        filemode="a",
        format="%(levelname)s [%(asctime)s %(name)s:%(lineno)d] %(message)s",
        datefmt="%y%m%d %H:%M:%S",
        level=getattr(logging, log_level.upper(), "INFO"),
    )
