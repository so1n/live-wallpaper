import datetime
import io
import logging
from itertools import product
from typing import Optional

from PIL import Image
from requests import Response  # type: ignore

from live_wallpaper.config import config
from live_wallpaper.lib import get_resolution, request_get
from live_wallpaper.module.base import BaseWallpaperModule

LOGGER: logging.Logger = logging.getLogger(__name__)


class Himawari8(BaseWallpaperModule):
    SITE = "himawari8"

    def __init__(self) -> None:
        self.padding_x: int = 0
        self.padding_y: int = 0
        super().__init__()

    def get_content(self, x: int, y: int, latest_str: str) -> Optional[bytes]:  # type: ignore
        url: str = "https://himawari8.nict.go.jp/img/D531106/{}d/{}/{}_{}_{}.png".format(
            config.module.module_config["level"],
            config.module.module_config["image_size"],
            latest_str,
            x,
            y,
        )
        LOGGER.info(f"<{self.SITE}> request url:{url}")
        content: bytes = request_get(url).content
        # If the tile data is 2867 bytes, it is a blank "No Image" tile.
        if content.__sizeof__() == 2867:
            LOGGER.error("No image available for {}.".format(latest_str))
            return None
        return content

    def get_id(self) -> Optional[str]:
        # TODO 改为获取id
        latest_ret: Response = request_get("https://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json")
        if latest_ret is None:
            return None

        raw_latest_date_str: str = latest_ret.json()["date"]
        latest_date: datetime.datetime = datetime.datetime.strptime(raw_latest_date_str, "%Y-%m-%d %H:%M:%S")
        LOGGER.info(f"<{self.SITE}> Latest date: {latest_date} GMT.")
        return latest_date.strftime("%Y/%m/%d/%H%M%S")

    def create_canvas(self) -> Image:
        resolution_x, resolution_y = get_resolution()
        if not (resolution_x or resolution_y):
            resolution_x = int(
                config.module.module_config["image_size"]
                * config.module.module_config["level"]
                / config.module.module_config["percent"]
            )
            resolution_y = int(
                config.module.module_config["image_size"]
                * config.module.module_config["level"]
                / config.module.module_config["percent"]
            )
        else:
            diff_resolution: float = (
                config.module.module_config["image_size"] * 2 / config.module.module_config["percent"]
            ) / resolution_y
            resolution_y = int(resolution_y * diff_resolution)
            resolution_x = int(resolution_x * diff_resolution)

        self.padding_x = int((resolution_x - config.module.module_config["image_size"] * 2) / 2)
        self.padding_y = int((resolution_y - config.module.module_config["image_size"] * 2) / 2)
        LOGGER.debug(
            f"<{self.SITE}> create canvas x:{resolution_x}, y{resolution_y};"
            f" padding x:{self.padding_x}, y:{self.padding_y}"
        )
        return Image.new("RGB", (resolution_x, resolution_y))

    def paste_canvas(self, canvas: Image, latest_str: str) -> None:
        for x, y in product(range(config.module.module_config["level"]), range(config.module.module_config["level"])):
            request_data = self.get_content(x, y, latest_str)
            if request_data is None:
                return None
            tile = Image.open(io.BytesIO(request_data))
            width = config.module.module_config["image_size"] * x + self.padding_x
            height = config.module.module_config["image_size"] * y + self.padding_y
            LOGGER.debug(
                "paste canvas start x:{}, end x:{},"
                " start y:{}, end y:{}".format(
                    width,
                    width + config.module.module_config["image_size"],
                    height,
                    config.module.module_config["image_size"] + y,
                )
            )
            canvas.paste(
                tile,
                (
                    width,
                    height,
                    width + config.module.module_config["image_size"],
                    config.module.module_config["image_size"] + height,
                ),
            )

    def save_image(self, path_filename: str, wallpaper_id: str) -> None:
        canvas: Image = self.create_canvas()
        self.paste_canvas(canvas, wallpaper_id)
        canvas.save(path_filename, "PNG")
