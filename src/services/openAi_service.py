import openai

from src.services.base_ai_service import BaseAiService
from src.promts import all_promts


class OpenAiService(BaseAiService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = openai.OpenAI(api_key=self._api_key, base_url="https://api.proxyapi.ru/openai/v1")

    async def analyze_image(self, base64_image):
        #надо как-то отрефакторить image_promt куда-то деть хз как
        image_promt = {
            "role": "user",
            "content": [
                {"type": "text", "text": "Что на изображении? Если на изображение не еда, тогда отвечай, что не можешь определить калории"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
            ],
        }
        promts = all_promts[:]
        promts.append(image_promt)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini", messages=promts, max_tokens=1000
        )
        return response.choices[0].message.content
