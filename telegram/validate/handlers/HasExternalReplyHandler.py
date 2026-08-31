import logging

from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType
from telegram.validate.handlers import AbstractHandler


class HasExternalReplyHandler(AbstractHandler):
    def _check_message(self, external_reply: object) -> bool:
        return isinstance(external_reply, bool) and external_reply

    async def handle(self, message: Context):
        if not isinstance(message.message.external_reply, bool):
            logging.debug("HasExternalReplyHandler пропущен: external_reply не установлен")
            return await super().handle(message)

        # Проверяем, есть ли external_reply в сообщении
        if self._check_message(message.message.external_reply):
            # Если есть external_reply, то автор сообщения должен быть забанен
            message.is_trusted = False
            message.execute_middleware = True
            message.punishment = PunishmentCommand(
                PunishmentType.BAN,
                reason="Обнаружен внешний ответ",
                source=type(self).__name__,
            )
            logging.info("HasExternalReplyHandler worked - user banned for external reply")
            return message

        # Если external_reply отсутствует, продолжаем цепочку
        return await super().handle(message)

    def is_available(self) -> bool:
        return True
