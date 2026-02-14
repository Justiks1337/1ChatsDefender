import logging

from aiogram.types import PhotoSize

from telegram.Message import Message
from utils.patterns.chain_of_responsibility import AbstractHandler
from utils.TextExtracter import TextExtracter
from telegram.dispatcher import bot
from utils.AIClient import AIClient
from telegram.punishments import warning

class ImageTextHandler(AbstractHandler):
    """
    Проверка текста с картинки
    """

    async def handle(self, message: Message):

        if message.message.photo is None:
            return super().handle(message)

        text_extracter = TextExtracter()
        photo_size: PhotoSize = message.message.photo[-1]
        photo = await bot.download(file=photo_size.file_id)
        photo_bytes = photo.read()
        photo_text: str = text_extracter.extract_text(photo_bytes)

        ai_client = AIClient()

        if ai_client.check_message(photo_text):
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("ImageTextHandler is worked now")
            return message

        return super().handle(message)
