import logging

from utils import AbstractHandler
from telegram.Message import Message
from telegram.punishments import warning


class ManySpacesHandler(AbstractHandler):
    async def handle(self, message: Message):

        text = message.message.text
        caption = message.message.caption

        if not (self.validate_text(text) and self.validate_text(caption)):
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("ManySpacesHandler is worked now")
            return message

        return await super().handle(message)

    def validate_text(self, text: str | None):
        if text is None:
            return True

        return not (text.count(" ") / len(text) * 100 > 35)
