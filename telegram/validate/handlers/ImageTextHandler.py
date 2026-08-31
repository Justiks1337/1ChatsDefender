import logging
from typing import Optional

import aiohttp

from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType
from telegram.validate.handlers.AbstractHandler import AbstractHandler


class ImageTextHandler(AbstractHandler):
    """
Проверка текста с картинки через OCR микросервис
    """

    def __init__(self):
        self.__available = True

        try:
            from utils.AIClient import AIClient
            from telegram.dispatcher import bot

            self.__ai_client = AIClient()
            self.__bot = bot
            self.ocr_service_url = "http://172.17.0.1:8000/extract-text"  # URL OCR микросервиса

        except ImportError:
            self.__available = False
            logging.error(
                "Не удалось загрузить ImageTextHandler из-за недостающей зависимости"
            )


    def _check_message(self, text: str) -> bool:
        return self.__ai_client.check_message(text)

    async def extract_text_from_image(self, image_bytes: bytes) -> Optional[str]:
        """
        Извлекает текст из изображения через OCR микросервис
        :param image_bytes: Байты изображения
        :return: Извлеченный текст или None в случае ошибки
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.ocr_service_url,
                    data={"image": image_bytes}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("text", "")
                    else:
                        logging.error(f"OCR service error: {response.status}")
                        return None
        except Exception as e:
            logging.error(f"Failed to extract text from image: {e}")
            return None

    async def handle(self, message: Context):

        if not isinstance(message.message.photo, list) or not message.message.photo:
            logging.debug("ImageTextHandler пропущен: photo не установлено")
            return await super().handle(message)

        photo_size = message.message.photo[-1]
        photo = await self.__bot.download(file=photo_size.file_id)
        photo_bytes = photo.read()
        # Извлекаем текст через OCR микросервис
        photo_text: str | None = await self.extract_text_from_image(photo_bytes)

        if photo_text is None:
            logging.warning("Failed to extract text from image")
            return await super().handle(message)

        if self._check_message(photo_text):
            message.is_trusted = False
            message.execute_middleware = True
            message.punishment = PunishmentCommand(
                PunishmentType.WARNING,
                reason="Недопустимый текст на изображении",
                source=type(self).__name__,
            )
            logging.info("ImageTextHandler is worked now")
            return message

        return await super().handle(message)

    def is_available(self) -> bool:
        return self.__available
