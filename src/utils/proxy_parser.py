import httpx
import requests
import json
import logging
from pathlib import Path

from config import settings

logger = logging.getLogger(__name__)

PROXY_FILE = Path(__file__).parent.parent.parent / "proxy.json"
print(PROXY_FILE)

def _build_proxy_url(item: dict) -> str:
    protocol = item.get("protocol", "http")
    return f"{protocol}://{item['ip']}:{item['port']}"

def _validate_proxy(url: str) -> bool:
    try:
        with httpx.Client(proxy=url, timeout=10.0) as client:
            response_gpt = client.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": "Bearer test_key"},
            )
            response_tg = client.get(f"https://api.telegram.org/bot{settings.bot_token}/getMe")
            return response_gpt.status_code == 401 and response_tg.status_code == 200
    except Exception as e:
        logger.debug(f"Прокси {url} недоступен: {e}")
        return False

def read_proxies_from_file() -> list[str]:
    if not PROXY_FILE.exists():
        raise FileNotFoundError("proxy.json не найден")
    
    with open(PROXY_FILE, "r") as f:
        data = json.load(f)
    
    return [_build_proxy_url(p) for p in data] if data else []

def download_proxies() -> list[str]:
    logger.info("Загрузка прокси с API...")
    data = requests.get(url=settings.proxy_api_url, timeout=30).json()

    valid_proxies = []
    for item in data:
        url = _build_proxy_url(item)
        if _validate_proxy(url):
            valid_proxies.append(item)

    logger.info(f"Найдено валидных прокси: {len(valid_proxies)}/{len(data)}")

    with open(PROXY_FILE, "w", encoding="utf-8") as f:
        json.dump(valid_proxies, f, indent=2, ensure_ascii=False)

    return [_build_proxy_url(p) for p in valid_proxies]


def get_valid_proxies() -> list[str]:
    if settings.proxy_url:
        logger.info("Найден приватный прокси, подключаюсь через него")
        return [settings.proxy_url]
    if not PROXY_FILE.exists():
        logger.warning("proxy.json не найден, загружаю новые...")
        return download_proxies()

    logger.info(f"Загрузка прокси из {PROXY_FILE}")
    with open(PROXY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        logger.warning("proxy.json пустой, загружаю новые...")
        return download_proxies()

    urls = [_build_proxy_url(p) for p in data]
    valid = [p for p in urls if _validate_proxy(p)]

    if valid:
        return valid

    logger.warning("Все прокси из файла недоступны, загружаю новые...")
    counter = 0
    while valid == []:
        counter += 1
        logger.warning(f"Пытаюсь скачать прокси попытка №{counter}")
        valid = download_proxies()
    return valid
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(get_valid_proxies())
