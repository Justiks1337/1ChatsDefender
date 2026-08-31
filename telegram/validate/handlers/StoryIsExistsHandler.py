import logging

from telegram.validate.Context import Context
from telegram.validate.handlers import AbstractHandler
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType


class StoryIsExistsHandler(AbstractHandler):
    def _check_message(self, story: object) -> bool:
        return isinstance(story, bool) and story

    async def handle(self, message: Context):
        if not isinstance(message.message.story, bool):
            logging.debug("StoryIsExistsHandler пропущен: story не установлен")
            return await super().handle(message)

        if self._check_message(message.message.story):
            message.is_trusted = False
            message.execute_middleware = True
            message.punishment = PunishmentCommand(
                PunishmentType.BAN,
                reason="Обнаружена история",
                source=type(self).__name__,
            )
            logging.debug("HistoryIsExistsHandler is working now")
            return message

        return await super().handle(message)

    def is_available(self) -> bool:
        return True
