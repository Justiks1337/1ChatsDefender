import logging

from telegram.Message import Message
from utils import AbstractHandler
from telegram.punishments import ban


class StoryIsExistsHandler(AbstractHandler):
    async def handle(self, message: Message):
        if not isinstance(message.message.story, bool):
            logging.debug("StoryIsExistsHandler пропущен: story не установлен")
            return await super().handle(message)

        if message.message.story:
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = ban(message.message)
            logging.debug("HistoryIsExistsHandler is working now")
            return message

        return await super().handle(message)
