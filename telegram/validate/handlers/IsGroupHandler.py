import logging

from telegram.validate.Context import Context
from telegram.validate.handlers import AbstractHandler


class IsGroupHandler(AbstractHandler):
    """Определяет, отправлено сообщение в группу или в личный чат.

    Если chat_id совпадает с идентификатором отправителя, останавливает
    проверки: правила модерации групп не должны применяться, например,
    к личному обращению пользователя к боту.
    """
    async def handle(self, message: Context):
        if not isinstance(message.message.chat_id, int) or not isinstance(message.message.from_user_id, int):
            logging.debug("IsGroupHandler пропущен: chat_id или from_user_id не установлен")
            return await super().handle(message)

        if message.message.chat_id == message.message.from_user_id:
            logging.debug("IsGroupHandler is working now")
            message.next_handler = False
            return message

        return await super().handle(message)

    def is_available(self) -> bool:
        return True
