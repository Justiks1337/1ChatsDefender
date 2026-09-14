import logging

from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType
from telegram.validate.handlers import AbstractHandler


class CheckInDatabaseHandler(AbstractHandler):
    """Запрашивает удаление сообщения, найденного в чёрном списке.

    Нужен для повторно публикуемого запрещённого текста: например,
    если уже известное спамное сообщение снова отправили в чат.
    Проверяет текст, а если он не задан строкой — подпись к сообщению.

    При точном совпадении с записью в БД назначает предупреждение,
    исполнение которого включает удаление сообщения.
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
