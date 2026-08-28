import logging

from utils import AbstractHandler
from telegram.Context import Context
from telegram.punishments import warning


class ManySpacesHandler(AbstractHandler):
    async def handle(self, message: Context):

        text = message.message.text
        caption = message.message.caption
        if not isinstance(text, str) and not isinstance(caption, str):
            logging.debug("ManySpacesHandler пропущен: text и caption не установлены")
            return await super().handle(message)

        if not (self.validate_text(text) and self.validate_text(caption)):
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("ManySpacesHandler is worked now")
            return message

        return await super().handle(message)

    def validate_text(self, text: object):
        if not isinstance(text, str) or not text:
            return True

        return not (text.count(" ") / len(text) * 100 > 35)
