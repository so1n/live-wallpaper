from typing import Tuple

from live_wallpaper.lib.bash import bash


def get_resolution() -> Tuple[int, int]:
    resolution = bash('xrandr --display :0 | grep "connected primary"')
    x, y = resolution.strip().split(" ")[3].split("+")[0].split("x")
    return int(x), int(y)
