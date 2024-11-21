import time

from modules.logger import logger

import requests
from requests import Response


ERROR_COOLDOWN: int = 2
_cache: dict = {}


class RequestError(Exception):
    pass


class API:
    FASTFLAGS: str = r"https://clientsettingscdn.roblox.com/v2/settings/application/PCDesktopClient"


# region get()
def get(url: str, attempts: int = 3, cache: bool = False) -> Response:
    if cache:
        if url in _cache:
            logger.debug(f"Cached GET request: {url}")
            return _cache[url]

    attempts -= 1

    try:
        logger.info(f"Attempting GET request: {url}")
        response: Response = requests.get(url, timeout=(5,15))
        response.raise_for_status()
        _cache[url] = response
        return response

    except Exception as e:
        logger.error(f"GET request failed: {url}, reason: {type(e).__name__}: {e}")

        if attempts <= 0:
            logger.error(f"GET request failed: {url}, reason: Too many attempts!")
            raise
        
        logger.warning(f"Remaining attempts: {attempts}")
        logger.info(f"Retrying in {ERROR_COOLDOWN} seconds...")
        time.sleep(ERROR_COOLDOWN)
        return get(url=url, attempts=attempts, cache=cache)
# endregion


# region post()
def post(url: str, json: dict, attempts: int = 3) -> Response:

    attempts -= 1

    try:
        logger.info(f"Attempting POST request: {url}")
        response: Response = requests.post(url, json=json, timeout=(5,15))
        response.raise_for_status()
        _cache[url] = response
        return response

    except Exception as e:
        logger.error(f"POST request failed: {url}, reason: {type(e).__name__}: {e}")

        if attempts <= 0:
            logger.error(f"POST request failed: {url}, reason: Too many attempts!")
            raise
        
        logger.warning(f"Remaining attempts: {attempts}")
        logger.info(f"Retrying in {ERROR_COOLDOWN} seconds...")
        time.sleep(ERROR_COOLDOWN)
        return post(url=url, json=json, attempts=attempts)
# endregion