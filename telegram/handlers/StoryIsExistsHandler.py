import logging

from telegram.Message import Message
from utils import AbstractHandler
from telegram.punishments import ban

class StoryIsExistsHandler(AbstractHandler):
    async def handle(self, message: Message):
        if message.message.story is not None:
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = ban(message.message)
            logging.debug("HistoryIsExistsHandler is working now")
            return message

        return await super().handle(message)
