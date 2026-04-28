from src.config import settings
from src.services.openAi_service import OpenAiService


class ServiceManager:
    #менеджер контекста
    async def __aenter__(self):
        self.openai = OpenAiService(settings.openai_api_key)
        #еще разные ai сервисы, типа deepseek
        return self
    async def __aexit__(self, *args, **kwargs):
        self.openai.close_client()
