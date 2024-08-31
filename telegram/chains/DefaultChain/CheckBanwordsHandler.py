import os
import re

from dotenv import load_dotenv

from telegram.Message import Message
from telegram.punishments import warning
from utils import AbstractHandler


load_dotenv()


class CheckBanwordsHandler(AbstractHandler):

    async def handle(self, message: Message):

        find = re.findall(os.getenv("BANWORD_REGEX"), message.message.text)

        if find:
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            return message

        return await super().handle(message)
