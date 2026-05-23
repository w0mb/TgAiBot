import random

import httpx

from src.utils.proxy_parser import get_valid_proxies


class BaseAiService:
    def __init__(self, api_key=None, **kwargs):
        self._api_key = api_key
        proxies = get_valid_proxies()
        if not proxies:
            raise Exception("get_valid_proxies() вернул неверные данные")
        self.http_client = httpx.Client(
            proxy=proxies[random.randint(0, len(proxies) - 1)]
        )

    def close_client(self):
        self.client.close()
