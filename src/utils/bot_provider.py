from aiogram import Bot


class BotProvider:
    _instance: Bot | None = None

    @classmethod
    def get_bot(cls) -> Bot:
        if cls._instance is None:
            raise RuntimeError("Bot not initialized")
        return cls._instance

    @classmethod
    def set_bot(cls, bot: Bot) -> None:
        cls._instance = bot
