import logging

from telegram.validate.handlers import AbstractHandler
from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType


class ManySpacesHandler(AbstractHandler):
    def _check_message(self, text: object, caption: object) -> bool:
        return not (self._validate_text(text) and self._validate_text(caption))

    async def handle(self, message: Context):

        text = message.message.text
        caption = message.message.caption
        if not isinstance(text, str) and not isinstance(caption, str):
            logging.debug("ManySpacesHandler пропущен: text и caption не установлены")
            return await super().handle(message)

        if self._check_message(text, caption):
            message.is_trusted = False
            message.execute_middleware = True
            message.punishment = PunishmentCommand(
                PunishmentType.WARNING,
                reason="Слишком много пробелов",
                source=type(self).__name__,
            )
            logging.info("ManySpacesHandler is worked now")
            return message

        return await super().handle(message)

    def _validate_text(self, text: object) -> bool:
        if not isinstance(text, str) or not text:
            return True

        return not (text.count(" ") / len(text) * 100 > 35)

    def is_available(self) -> bool:
        return True
