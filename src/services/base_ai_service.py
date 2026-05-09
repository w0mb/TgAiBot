import random
import httpx

from src.utils.proxy_parser import read_proxies_from_file


class BaseAiService:
    def __init__(self, api_key=None, **kwargs):
        self._api_key = api_key

        proxies = read_proxies_from_file()
        if proxies is None or proxies == []:
            raise Exception("get_valid_proxies() вернул неверные данные")

        # хз как сделать иначе (без рандома всмысле)
        self.http_client = httpx.Client(
            proxy=proxies[random.randint(0, len(proxies) - 1)]
        )

    def close_client(self):
        self.client.close()
