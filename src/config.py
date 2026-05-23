from pathlib import Path
from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    bot_token: str
    openai_api_key: str
    postgres_user: str
    postgres_pass: str
    postgres_host: str
    postgres_port: str
    postgres_db_name: str
    openai_url: str

    redis_port: str
    redis_host: str

    proxy_url: str | None = None

    @property
    def proxy_api_url(self):
        return self.__proxy_api_url

    @proxy_api_url.setter
    def proxy_api_url(self, url):
        self.__proxy_api_url = url

    @property
    def postgres_url(self):
        return self.__postgres_url

    @postgres_url.setter
    def postgres_url(self, url):
        self.__postgres_url = url

    @property
    def redis_url(self):
        return self.__redis_url

    @redis_url.setter
    def redis_url(self, redis_url):
        self.__redis_url = redis_url

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env"
    )


settings = Settings()
settings.proxy_api_url = "https://api.best-proxies.ru/proxylist.json?key=developer&google=1&country=GB,US,BR&type=https&limit=40"
settings.postgres_url = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_pass}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db_name}"
settings.redis_url = f"redis://{settings.redis_host}:{settings.redis_port}"
