import logging

from utils import AbstractHandler
from telegram.Message import Message


class IsPremiumHandler(AbstractHandler):
    async def handle(self, message: Message):

        if not message.message.from_user_is_premium:
            logging.debug("IsPremiumHandler worked now")
            return message

        return await super().handle(message)
