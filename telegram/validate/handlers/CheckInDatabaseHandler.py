import logging

from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType
from telegram.validate.handlers import AbstractHandler


class CheckInDatabaseHandler(AbstractHandler):
    """
    Хендлер проверяет наличие текста сообщения в черном списке
    Если текст сообщения присутствует в черном списке, сообщение блокируется
    """

    def __init__(self):
        self.__available = True

        try:
            from utils.database.connection import DatabaseConnection
            self.__connection = DatabaseConnection()
        except ImportError:
            self.__available = False
            logging.error(
                "Не удалось загрузить CheckInDatabaseHandler из-за недостающей зависимости DatabaseConnection!")

    async def _check_message(self, text: str) -> bool:
        return await self.__connection.is_message_banned(text)

    async def handle(self, message: Context):
        text = message.message.text
        if not isinstance(text, str):
            text = message.message.caption
        if not isinstance(text, str):
            logging.debug("CheckInDatabaseHandler пропущен: текст и подпись не установлены")
            return await super().handle(message)

        if await self._check_message(text):
            message.is_trusted = False
            message.execute_middleware = True
            message.punishment = PunishmentCommand(
                PunishmentType.WARNING,
                reason="Сообщение найдено в базе запрещённых сообщений",
                source=type(self).__name__,
            )
            logging.info("CheckInDatabaseHandler is worked now")
            return message

        return await super().handle(message)

    def is_available(self) -> bool:
        return self.__available
