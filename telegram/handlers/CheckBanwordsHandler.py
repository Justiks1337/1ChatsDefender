import os
import re
import logging

from dotenv import load_dotenv

from telegram.Message import Message
from telegram.punishments import warning
from utils import AbstractHandler


load_dotenv()


class CheckBanwordsHandler(AbstractHandler):

    def __init__(self, text=os.getenv("BANWORD_REGEX")):
        self.pattern = re.compile(text, re.IGNORECASE | re.UNICODE)

    async def handle(self, message: Message):
        find = None
        caption_find = None

        if message.message.text is not None:
            find = self.pattern.search(message.message.text)
        if message.message.caption is not None:
            caption_find += self.pattern.search(message.message.caption)

        if find or caption_find:
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("CheckBanwordsHandler handler worked now")
            return message

        return await super().handle(message)
