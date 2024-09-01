import logging

from telegram.Message import Message
from utils import AbstractHandler


class IsGroupHandler(AbstractHandler):
    """
    This handler check, message send in a group, or in a dm
    """
    async def handle(self, message: Message):
        if message.message.chat.id == message.message.from_user.id:
            logging.debug("IsGroupHandler is working now")
            return message

        return await super().handle(message)
