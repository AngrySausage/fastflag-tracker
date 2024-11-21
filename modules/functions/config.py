import os
import json
from typing import Literal, Optional

from modules.logger import logger


ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONFIG: str = os.path.join(ROOT, "config", "config.json")


def get(key: Optional[Literal["url", "error_url", "username", "avatar_url"]] = None) -> Optional[str] | dict:
    if not os.path.isfile(CONFIG):
        raise FileNotFoundError("No such file or directory: config/config.json")
    
    try:
        with open(CONFIG, "r") as file:
            data: dict = json.load(file)

    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError while reading config.json: {e}")
        raise

    if key is None:
        return data

    if key not in data:
        logger.error(f"Could not find \"{key}\" in config.json")
        raise KeyError(f"Could to find \"{key}\" in config.json")
    
    return data[key]


def get_url() -> Optional[str]:
    return get("url")


def get_error_url() -> Optional[str]:
    return get("error_url")


def get_username() -> Optional[str]:
    return get("username")


def get_avatar_url() -> Optional[str]:
    return get("avatar_url")