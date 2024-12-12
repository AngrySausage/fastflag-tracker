import time

from modules.logger import logger

import requests
from requests import Response


ERROR_COOLDOWN: int = 2
_cache: dict = {}


class RequestError(Exception):
    pass

# listed in order of MaximumADHD's clientappsettings jsons
class API:
    FASTFLAGS: list[str] = [
        r"https://clientsettingscdn.roblox.com/v2/settings/application/AndroidApp",
        r"https://clientsettingscdn.roblox.com/v2/settings/application/MacDesktopClient",
        r"https://clientsettingscdn.roblox.com/v2/settings/application/PCDesktopClient",
        r"https://clientsettingscdn.roblox.com/v2/settings/application/PlayStationClient",
        r"https://clientsettingscdn.roblox.com/v2/settings/application/UWPApp",
        r"https://clientsettingscdn.roblox.com/v2/settings/application/XboxClient",
        r"https://clientsettingscdn.roblox.com/v2/settings/application/iOSApp"
    ]

# region get()
def get(url: str, attempts: int = 3, cache: bool = False) -> Response:
    if cache:
        if url in _cache:
            logger.debug(f"Cached GET request: {url}")
            return _cache[url]

    attempts -= 1

    try:
        logger.info(f"Attempting GET request: {url}")
        response: Response = requests.get(url, timeout=(5, 15))
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


# region get_multiple()
def get_multiple(urls: list[str], attempts: int = 3, cache: bool = False) -> dict[str, Response]:
    """
    Fetch responses from multiple URLs.
    Returns a dictionary mapping URLs to their responses.
    """
    responses = {}
    for url in urls:
        try:
            response = get(url, attempts=attempts, cache=cache)
            responses[url] = response
        except Exception as e:
            logger.error(f"Failed to GET {url}: {type(e).__name__}: {e}")
            responses[url] = None
    return responses
# endregion


# region post()
def post(url: str, json: dict, attempts: int = 3) -> Response:

    attempts -= 1

    try:
        logger.info(f"Attempting POST request: {url}")
        response: Response = requests.post(url, json=json, timeout=(5, 15))
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


# Example usage
if __name__ == "__main__":
    # Fetch responses for all FASTFLAGS URLs
    responses = get_multiple(API.FASTFLAGS, attempts=3, cache=True)

    # Log responses
    for url, response in responses.items():
        if response:
            logger.info(f"Response from {url}: {response.status_code}")
        else:
            logger.error(f"Failed to fetch data from {url}")