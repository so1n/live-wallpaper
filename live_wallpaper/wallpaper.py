import logging
import os
import subprocess
from typing import Optional, Tuple

from live_wallpaper import module
from live_wallpaper.config import Config, get_config
from live_wallpaper.lib.bash import bash
from live_wallpaper.lib.log import init_logging
from live_wallpaper.lib.path import get_file_path

config: Config = get_config()
init_logging(config.log_path, config.log_level)
LOGGER: logging.Logger = logging.getLogger(__name__)


class Wallpaper(object):
    module: module.BaseWallpaperModule

    def __init__(self) -> None:
        self.path_filename: Optional[str] = None
        self.path = get_file_path(__file__) + "/"

    @staticmethod
    def set_environ() -> None:
        """fix crontab environ
        https://stackoverflow.com/questions/10374520/gsettings-with-cron
        /19666729#19666729"""
        os.environ["DISPLAY"] = ":0"
        pid: str = subprocess.check_output(["pgrep", "dde-session"]).decode("utf-8").strip()
        cmd: str = "grep -z DBUS_SESSION_BUS_ADDRESS /proc/{}/environ|cut -d= -f2-".format(pid)
        os.environ["DBUS_SESSION_BUS_ADDRESS"] = (
            subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8").strip().replace("\0", "")
        )

    def set_wallpaper(self, path_filename: str) -> None:
        display: str = bash("xrandr|grep 'connected primary'|awk '{print $1}'").strip()
        bash(config.system.change_wallpaper_bash.format(display=display, file=path_filename))
        wallpaper_result_list = bash(config.system.set_wallpaper_bash)
        LOGGER.info(f"{self.module.SITE}> Now wallpaper:{wallpaper_result_list}")

    def gen_filename(self, wallpaper_id: str) -> Tuple[str, str]:
        filename: str = wallpaper_id + ".png"
        path_filename: str = self.path + "images/" + self.module.SITE + "_" + filename
        return filename, path_filename

    @staticmethod
    def check_file(path_filename: str) -> bool:
        exists = os.path.exists(path_filename)
        return exists

    def rm(self) -> None:
        if config.system.rm_bash:
            bash(config.system.rm_bash)
        else:
            if config.system.rm_time:
                rm_time = "-mmin +" + str(config.system.rm_time)
            elif config.system.rm_time == "":
                rm_time = "-mmin +" + config.module.module_interval * 2
            else:
                LOGGER.error("exec rm fail, please run doctor check config.json")
                return
            bash("find {path}images/ -name '*.png' {rm_time} | xargs rm".format(path=self.path, rm_time=rm_time))

    def run(self) -> None:
        self.set_environ()
        LOGGER.debug("crontab environ:{}".format(os.environ))
        self.module = getattr(module, config.module.module_name, None)()  # noqa
        if self.module is None:
            LOGGER.error(f"Not found module: {config.module.module_name}")
            return
        LOGGER.debug("Find module:{}".format(self.module))

        wallpaper_id: Optional[str] = self.module.get_id()
        if wallpaper_id is None:
            LOGGER.error("network error, can't found id.")
            return

        filename, path_filename = self.gen_filename(wallpaper_id)
        if self.check_file(path_filename):
            LOGGER.warning(f"<{self.module.SITE}> {path_filename} is already exists")
            return None

        self.module.save_image(path_filename, wallpaper_id)
        LOGGER.info(f"<{self.module.SITE}> save wallpaper:{path_filename}")
        self.set_wallpaper(path_filename)
        self.rm()


if __name__ == "__main__":
    wallpaper = Wallpaper()
    wallpaper.run()
