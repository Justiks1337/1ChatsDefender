import logging

from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType
from telegram.validate.handlers.AbstractHandler import AbstractHandler


class HasInlineKeyboardMarkupHandler(AbstractHandler):
    """
    В чат отправляются сообщения с кнопками, созданными при помощи ботов и телеграмм-каналов.
    Этот хандлер удаляет подобные сообщения
    """

    def _check_message(self, reply_markup: object) -> bool:
        return isinstance(reply_markup, bool) and reply_markup

    async def handle(self, message: Context):
        if not isinstance(message.message.reply_markup, bool):
            logging.debug("HasInlineKeyboardMarkupHandler пропущен: reply_markup не установлен")
            return await super().handle(message)

        # Проверяем наличие markup
        if not self._check_message(message.message.reply_markup):
            return await super().handle(message)

        message.is_trusted = False
        message.execute_middleware = True
        message.punishment = PunishmentCommand(
            PunishmentType.BAN,
            reason="Обнаружена встроенная клавиатура",
            source=type(self).__name__,
        )
        logging.debug("HasInlineKeyboardMarkupHandler is work now!")
        return message

    def is_available(self) -> bool:
        return True
