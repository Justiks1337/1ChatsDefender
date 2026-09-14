import os
import re
import logging

from dotenv import load_dotenv

from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType
from telegram.validate.handlers import AbstractHandler

load_dotenv()


class RegexHandler(AbstractHandler):

    def __init__(self, text=os.getenv("BANWORD_REGEX")):
        if not text:
            raise AttributeError("Не передан regex в RegexHandler")

        self.pattern = re.compile(text, re.IGNORECASE | re.UNICODE)

    def _check_message(self, text: object, caption: object) -> bool:
        text_match = isinstance(text, str) and self.pattern.search(text) is not None
        caption_match = isinstance(caption, str) and self.pattern.search(caption) is not None
        return text_match or caption_match

    async def handle(self, message: Context):
        text = message.message.text
        caption = message.message.caption
        if not isinstance(text, str) and not isinstance(caption, str):
            logging.debug("RegexHandler пропущен: text и caption не установлены")
            return await super().handle(message)

        if self._check_message(text, caption):
            message.punishment = PunishmentCommand(
                PunishmentType.WARNING,
                reason="Обнаружены запрещённые слова",
                source=type(self).__name__,
            )
            logging.info("RegexHandler handler worked now")
            return message

        return await super().handle(message)

    def is_available(self) -> bool:
        return True
