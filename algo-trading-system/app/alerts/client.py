import httpx

from app.core.config import get_settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class TelegramClient:
    def __init__(self) -> None:
        settings = get_settings()

        self.bot_token = (
            settings.telegram_bot_token
        )

        self.chat_id = (
            settings.telegram_chat_id
        )

        self.base_url = (
            f"https://api.telegram.org/bot"
            f"{self.bot_token}"
        )

    async def send_message(
        self,
        message: str,
    ) -> None:
        if not self.bot_token:
            logger.warning(
                "telegram_bot_token_missing"
            )
            return

        if not self.chat_id:
            logger.warning(
                "telegram_chat_id_missing"
            )
            return

        url = (
            f"{self.base_url}/sendMessage"
        )

        payload = {
            "chat_id": self.chat_id,
            "text": message,
        }

        try:
            async with httpx.AsyncClient(
                timeout=10,
            ) as client:
                response = await client.post(
                    url,
                    json=payload,
                )

                response.raise_for_status()

            logger.info(
                "telegram_message_sent"
            )

        except Exception as exc:
            logger.exception(
                "telegram_message_failed",
                error=str(exc),
            )