import os
import pathlib
from typing import Optional

from pydantic import BaseModel

from live_wallpaper.lib.config import Config as _Config
from live_wallpaper.lib.current_user import get_current_user

current_file_path: str = os.path.split(os.path.realpath(__file__))[0]
config_path: str = f"/home/{get_current_user()}/.config/live-wallpaper/"
config_filename: str = f"/home/{get_current_user()}/.config/live-wallpaper/live-wallpaper.json"
default_config_filename: str = f"{current_file_path}/default_config.json"
cache_path: str = f"/home/{get_current_user()}/.cache/live-wallpaper/"

config_path_ojb: pathlib.Path = pathlib.Path(config_path)
cache_path_obj: pathlib.Path = pathlib.Path(cache_path)
if not cache_path_obj.exists():
    cache_path_obj.mkdir(parents=True)
if not config_path_ojb.exists():
    config_path_ojb.mkdir(parents=True)


def reset_config(filename: Optional[str] = None) -> None:
    if not filename:
        filename = default_config_filename
    with open(filename) as df:
        with open(config_filename, mode="w+") as nf:
            for line in df.readlines():
                nf.write(line)


if not pathlib.Path(config_filename).exists():
    reset_config()


class Config(_Config):
    class ModuleConfigModel(BaseModel):
        module_name: str
        module_interval: str
        module_config: dict

    class SystemConfigModel(BaseModel):
        change_wallpaper_bash: str
        set_wallpaper_bash: str
        crontab_comment: str
        rm_bash: str
        nice_bash: str
        cpu_limit_bash: str
        rm_time: int = 60

    log_level: str = "INFO"
    log_path: str = cache_path + "/log"
    module: ModuleConfigModel
    system: SystemConfigModel


config: Config = Config(config_filename)
