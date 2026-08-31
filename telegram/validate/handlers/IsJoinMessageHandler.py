import logging

from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType
from telegram.validate.handlers import AbstractHandler


class IsJoinMessageHandler(AbstractHandler):
    def _check_message(self, new_chat_members: object) -> bool:
        return isinstance(new_chat_members, bool) and new_chat_members

    async def handle(self, message: Context) -> Context:
        if not isinstance(message.message.new_chat_members, bool):
            logging.debug("IsJoinMessageHandler пропущен: new_chat_members не установлен")
            return await super().handle(message)

        if self._check_message(message.message.new_chat_members):
            message.is_trusted = False
            message.punishment = PunishmentCommand(
                PunishmentType.DELETE,
                reason="Служебное сообщение о вступлении",
                source=type(self).__name__,
            )
            logging.info("IsJoinMessageHandler is working now")
            return message

        return await super().handle(message)

    def is_available(self) -> bool:
        return True
