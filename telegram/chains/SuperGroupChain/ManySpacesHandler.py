import logging

from utils import AbstractHandler
from telegram.Message import Message
from telegram.punishments import warning


class ManySpacesHandler(AbstractHandler):
    async def handle(self, message: Message):

        text = message.message.text

        if text.count(" ") / len(text) * 100 > 35:
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("ManySpacesHandler is worked now")
            return message

        return await super().handle(message)