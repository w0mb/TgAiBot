import httpx
import requests
import json
import logging

from config import settings

logger = logging.getLogger()


def download_proxies() -> list[dict]:
    data = requests.get(url=settings.proxy_api_url).json()
    valid_proxy = []
    for d in data:
        url = "http://" + d["ip"] + ":" + str(d["port"])
        with httpx.Client(proxy=url, timeout=10.0) as client:
            try:
                response = client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": "Bearer test_key"},
                )
                if response.status_code == 401:
                    valid_proxy.append(d)
            except:
                continue

    with open("../proxy.json", "w", encoding="utf-8") as file:
        json.dump(valid_proxy, file, indent=2, ensure_ascii=False)
    return valid_proxy


def get_valid_proxies() -> list[str]:
    urls = []
    with open("../proxy.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        logger.info("Использую прокси из файла proxy.json")
        if data:
            for i in data:
                urls.append("http://" + i["ip"] + ":" + str(i["port"]))
        else:
            logger.info("Файл не найден или пустой, загружаю новые прокси")
            return download_proxies()
    return urls


if __name__ == "__main__":
    get_valid_proxies()
