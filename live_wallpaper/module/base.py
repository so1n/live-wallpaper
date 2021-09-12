from typing import Any, Optional


class BaseWallpaperModule(object):
    SITE: str = "base"

    def get_content(self, *args: Any) -> Optional[bytes]:
        pass

    def get_id(self) -> Optional[str]:
        pass

    def save_image(self, path_filename: str, wallpaper_id: str) -> None:
        pass
