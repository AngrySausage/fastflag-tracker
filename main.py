# FastFlag Tracker - version 1.0.0
# Made by TheKliko
# 
# Make sure the requests library is installed before running this program (This can be done by running install_libraries.bat)

import os
import sys
import copy
import time
from typing import Optional
import json
import traceback


ROOT: str = os.path.dirname(__file__)
LIBRARIES_PATH: str = os.path.join(ROOT, "libraries")
sys.path.insert(0, LIBRARIES_PATH)

from requests.exceptions import ConnectionError


from modules.logger import logger
from modules.webhook import WebHook, EmbedColor
from modules.functions.get_fastflags import get_fastflags
from modules.request import RequestError


CONFIG: str = os.path.join(ROOT, "config", "config.json")
BACKUP: str = os.path.join(ROOT, "backup.json")

# Run every 2 minutes
# Reduce this cooldown at your own risk, setting it too low may result in getting ratelimited
COOLDOWN: float | int = 2 * 60


def main() -> None:
    # Check for config file
    if not os.path.isfile(CONFIG):
        raise FileNotFoundError("No such file or directory: config/config.json")

    webook: WebHook = WebHook()

    # Continue from backup, if available
    old_flags: Optional[dict] = None
    try:
        old_flags = restore_backup()
    except Exception as e:
        logger.warning(f"Failed to restore backup! {type(e).__name__}: {e}")

    try:  # Main loop
        print("Tracking FastFlags...")
        while True:
            try:
                current_flags: dict = get_fastflags()
            except RequestError as e:
                logger.error(f"{type(e).__name__}: {e}")
                time.sleep(COOLDOWN)
                continue

            if old_flags is not None and old_flags != current_flags:
                new_flags: dict = {
                    key: value
                    for key, value in current_flags.items()
                    if key not in old_flags
                }

                removed_flags: list[str] = [
                    key for key in old_flags
                    if key not in current_flags
                ]

                changed_flags: list[dict] = [
                    {
                        "key": key,
                        "old": {key: old_flags[key]},
                        "current": {key: current_flags[key]}
                    }
                    for key in old_flags
                    if key in current_flags
                    and old_flags[key] != current_flags[key]
                ]

                embeds: list[dict] = []
                if new_flags:
                    string = f"```json\n{json.dumps(new_flags, indent=2)}```"
                    if len(string) > webook.EMBED_DESCRIPTION_CHARACTER_LIMIT:
                        embeds.append(webook.get_embed(title="New FFlags", description="Content exceeds character limit!", color=EmbedColor.GREEN))
                    else:
                        embeds.append(webook.get_embed(title="New FFlags", description=string, color=EmbedColor.GREEN))

                if removed_flags:
                    string = f"{'\n'.join([f'• {flag}' for flag in removed_flags])}"
                    if len(string) > webook.EMBED_DESCRIPTION_CHARACTER_LIMIT:
                        embeds.append(webook.get_embed(title="Removed FFlags", description="Content exceeds character limit!", color=EmbedColor.RED))
                    else:
                        embeds.append(webook.get_embed(title="Removed FFlags", description=string, color=EmbedColor.RED))
                
                if changed_flags:
                    string = f"{
                        '\n\n'.join([
                            f"**{flag["key"]}**\nBefore: `\"{flag["old"][flag["key"]]}\"`\nAfter: `\"{flag["current"][flag["key"]]}\"`"
                            for flag in changed_flags
                        ])
                    }"
                    if len(string) > webook.EMBED_DESCRIPTION_CHARACTER_LIMIT:
                        embeds.append(webook.get_embed(title="Changed FFlags", description="Content exceeds character limit!", color=EmbedColor.YELLOW))
                    else:
                        embeds.append(webook.get_embed(title="Changed FFlags", description=string, color=EmbedColor.YELLOW))
                
                if embeds:
                    try:
                        webook.send(embeds=embeds)
                    except ConnectionError as e:
                        logger.error(f"{type(e).__name__}: {e}")
                        time.sleep(COOLDOWN)
                        continue

            old_flags = copy.deepcopy(current_flags)
            save_backup(current_flags)

            time.sleep(COOLDOWN)
    
    except Exception as e:
        logger.critical(f"{type(e).__name__}: {e}")
        logger.debug(f"Traceback:\n{''.join(traceback.format_exception(e))}")
        webook.send_error(e)


def restore_backup() -> dict | None:
    if not os.path.isfile(BACKUP):
        return None
    
    with open(BACKUP, "r") as file:
        data: dict = json.load(file)
    
    logger.debug("Data restored from backup.json")
    return data


def save_backup(data: dict) -> None:
    try:
        with open(BACKUP, "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        logger.error(f"Failed to save backup! {type(e).__name__}: {e}")
        raise


if __name__ == "__main__":
    main()