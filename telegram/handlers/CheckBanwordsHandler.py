import os
import re
import logging

from dotenv import load_dotenv

from telegram.Context import Context
from telegram.punishments import warning
from utils import AbstractHandler


load_dotenv()


class CheckBanwordsHandler(AbstractHandler):

    def __init__(self, text=os.getenv("BANWORD_REGEX")):
        self.pattern = re.compile(text, re.IGNORECASE | re.UNICODE)

    async def handle(self, message: Context):
        text = message.message.text
        caption = message.message.caption
        if not isinstance(text, str) and not isinstance(caption, str):
            logging.debug("CheckBanwordsHandler пропущен: text и caption не установлены")
            return await super().handle(message)

        find = None
        caption_find = None

        if isinstance(text, str):
            find = self.pattern.search(text)
        if isinstance(caption, str):
            caption_find = self.pattern.search(caption)

        if find or caption_find:
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("CheckBanwordsHandler handler worked now")
            return message

        return await super().handle(message)
