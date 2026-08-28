import logging

from telegram.Message import Message
from utils import AbstractHandler


class IsGroupHandler(AbstractHandler):
    """
    This handler check, message send in a group, or in a dm
    """
    async def handle(self, message: Message):
        if not isinstance(message.message.chat_id, int) or not isinstance(message.message.from_user_id, int):
            logging.debug("IsGroupHandler пропущен: chat_id или from_user_id не установлен")
            return await super().handle(message)

        if message.message.chat_id == message.message.from_user_id:
            logging.debug("IsGroupHandler is working now")
            message.next_handler = False
            return message

        return await super().handle(message)
