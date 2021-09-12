import logging
import time
from typing import Optional

import requests  # type: ignore
from requests import Response

chrome_headers = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6",
}


def request_get(url: str) -> Response:
    """Get response through request.get method (retry at most 3 times)"""
    exception: Optional[Exception] = None

    for i in range(1, 4):  # retry max 3 times
        try:
            return requests.get(url=url, headers=chrome_headers, verify=False)
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
        ) as e:
            exception = e
        except Exception as e:
            exception = e
        logging.info("[{}/3] Retrying to download '{}'...".format(i, url))
        time.sleep(1 * i * i)

    if not exception:
        exception = RuntimeError("requests get error")

    raise exception
