import logging

from telegram.Message import Message
from utils import AbstractHandler


class IsGroupHandler(AbstractHandler):
    """
    This handler check, message send in a group, or in a dm
    """
    async def handle(self, message: Message):
        if message.message.chat_id == message.message.from_user_id:
            logging.debug("IsGroupHandler is working now")
            message.next_handler = False
            return message

        return await super().handle(message)
