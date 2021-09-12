import logging


def init_logging(path_str: str, log_level: str) -> None:
    log_filename: str = path_str + "/log/live-wallpaper.log"
    logging.basicConfig(
        filename=log_filename,
        filemode="a",
        format="%(levelname)s [%(asctime)s %(name)s:%(lineno)d] %(message)s",
        datefmt="%y%m%d %H:%M:%S",
        level=getattr(logging, log_level.upper(), "INFO"),
    )
