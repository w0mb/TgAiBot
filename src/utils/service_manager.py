from src.config import settings
from src.services.openAi_service import OpenAiService


class ServiceManager:
    async def __aenter__(self):
        self.openai = OpenAiService(api_key=settings.openai_api_key, base_url=settings.openai_url)
        return self

    async def __aexit__(self, *args, **kwargs):
        self.openai.close_client()
