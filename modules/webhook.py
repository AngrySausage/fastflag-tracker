import sys
import traceback
from typing import Optional

from modules.functions import config
from modules import request


class WebHookException(Exception):
    pass


class EmbedColor:
    GREEN: str = "#00F02E"
    YELLOW: str = "#FFB518"
    RED: str = "#FF0000"


class WebHook:
    url: list[str] | str
    username: Optional[str]
    error_url: Optional[list[str] | str]
    avatar_url: Optional[str]

    EMBED_DESCRIPTION_CHARACTER_LIMIT: int = 4096

    def __init__(self) -> None:
        self._update_variables()


    def _update_variables(self) -> None:
        data: dict = config.get()
        
        self.url = data["url"]
        self.username = data["username"]
        self.error_url = data["error_url"]
        self.avatar_url = data["avatar_url"]

        if self.url is None:
            raise WebHookException("webhook url may not be None")
    

    def get_embed(self, title: Optional[str] = None, description: Optional[str] = None, fields: Optional[list[dict]] = None, color: Optional[str] = None) -> dict:
        embed: dict = {}
        if title is not None:
            embed["title"] = title
        if description is not None:
            if len(description) > self.EMBED_DESCRIPTION_CHARACTER_LIMIT:
                raise WebHookException("Embed description length exceeds character limit")
            embed["description"] = description
        if color is not None:
            embed["color"] = int(color.removeprefix("#"), 16)

        if fields is not None:
            embed["fields"] = []
            for field in fields:
                name: str = field["name"]
                value: str = field["value"]
                embed["fields"].append({"name": name, "value": value})

        return embed
    

    def send(self, content: Optional[str] = None, embeds: Optional[list[dict]] = None, url_override: Optional[list[str]|str] = None) -> None:
        self._update_variables()
        
        json: dict = {"content": content}
        if self.username is not None:
            json["username"] = self.username
        if self.avatar_url is not None:
            json["avatar_url"] = self.avatar_url
        if embeds is not None:
            json["embeds"] = embeds
        
        if content is None and embeds is None:
            raise WebHookException("content and embeds may not both be None")

        if url_override is not None:
            if isinstance(url_override, list):
                for url in url_override:
                    request.post(url, json)
            else:
                request.post(url_override, json)
        elif isinstance(self.url, list):
            for url in self.url:
                request.post(url, json)
        else:
            request.post(self.url, json)
    

    def send_error(self, *args) -> None:
        if self.error_url is None:
            return

        error_message: str = "".join(traceback.format_exception(*args))
        embed: dict = self.get_embed(title="Something went wrong!", description=f"```python\n{error_message}\n```", color=EmbedColor.RED)
        self.send(content="Shutting down...", embeds=[embed], url_override=self.error_url)
        sys.exit(1)


    def send_message(self, message: str) -> None:
        self.send(content=message)