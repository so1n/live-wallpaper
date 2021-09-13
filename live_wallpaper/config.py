import pathlib

from pydantic import BaseModel

from live_wallpaper.lib.config import Config as _Config
from live_wallpaper.lib.config import Json
from live_wallpaper.lib.current_user import get_current_user

config_path: str = f"/home/{get_current_user()}/.config/live-wallpaper/"
config_filename: str = f"/home/{get_current_user()}/.config/live-wallpaper/live-wallpaper.json"
cache_path: str = f"/home/{get_current_user()}/.cache/live-wallpaper/"

config_path_ojb: pathlib.Path = pathlib.Path(config_path)
cache_path_obj: pathlib.Path = pathlib.Path(cache_path)
if not cache_path_obj.exists():
    cache_path_obj.mkdir(parents=True)
if not config_path_ojb.exists():
    config_path_ojb.mkdir(parents=True)


def reset_config() -> None:
    with open("default_config.json") as df:
        with open(config_filename, mode="w+") as nf:
            for line in df.readlines():
                nf.write(line)


if not pathlib.Path(config_filename).exists():
    reset_config()


class Config(_Config):
    class ModuleConfigModel(BaseModel):
        module_name: str
        module_interval: str
        module_config: dict = Json.i()

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
