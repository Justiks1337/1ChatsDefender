import logging
from typing import Optional

import aiohttp
from aiogram.types import PhotoSize

from telegram.Message import Message
from utils.patterns.chain_of_responsibility import AbstractHandler
from telegram.dispatcher import bot
from utils.AIClient import AIClient
from telegram.punishments import warning


class ImageTextHandler(AbstractHandler):
    """
    Проверка текста с картинки через OCR микросервис
    """

    def __init__(self):
        self.ocr_service_url = "http://localhost:8000/extract-text"  # URL OCR микросервиса

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

    async def handle(self, message: Message):

        if message.message.photo is None:
            return super().handle(message)

        photo_size: PhotoSize = message.message.photo[-1]
        photo = await bot.download(file=photo_size.file_id)
        photo_bytes = photo.read()
        
        # Извлекаем текст через OCR микросервис
        photo_text: str = await self.extract_text_from_image(photo_bytes)

        if photo_text is None:
            logging.warning("Failed to extract text from image")
            return await super().handle(message)

        ai_client = AIClient()

        if ai_client.check_message(photo_text):
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("ImageTextHandler is worked now")
            return message

        return await super().handle(message)
