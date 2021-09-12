import pathlib

from pydantic import BaseModel

from live_wallpaper.lib.config import Config as _Config
from live_wallpaper.lib.config import Json
from live_wallpaper.lib.current_user import get_current_user

config_filename: str = f"/home/{get_current_user()}/.config/live-wallpaper/live-wallpaper.json"
cache_path: str = f"/home/{get_current_user()}/.cache/live-wallpaper/"
if not pathlib.Path(config_filename).exists():
    with open("default_config.json") as df:
        with open(config_filename) as nf:
            for line in df.readlines():
                nf.write(line)


class Config(_Config):
    class ModuleConfigModel(BaseModel):
        module_name: str
        module_interval: str
        module_config: dict = Json.i()

    class SystemConfigModel(BaseModel):
        change_wallpaper_bash: str
        change_wallpaper_bash_bak: str
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
