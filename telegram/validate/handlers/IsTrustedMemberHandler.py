import time
import os
import logging

from telegram.validate.Context import Context
from telegram.validate.handlers.AbstractHandler import AbstractHandler


class IsTrustedMemberHandler(AbstractHandler):
    """
    Проверка, является ли пользователь доверенным
    Пользователем является доверенным если он находится в чатах более IS_TRUSTED_MEMBER секунд
    """

    # Время в секундах, после которого пользователь считается доверенным и игнорируется
    IS_TRUSTED_MEMBER = int(os.environ['IS_TRUSTED_MEMBER'])

    def __init__(self):
        self.__is_available = True

        try:
            from utils.database.connection import DatabaseConnection
            self.__database_connection = DatabaseConnection()
        except ImportError:
            self.__is_available = False
            logging.error("Не удалось загрузить IsTrustedMemberHandler из-за недостающей зависимости: \nfrom utils.database.connection import DatabaseConnection")

    async def handle(self, message: Context):
        if not isinstance(message.message.from_user_id, int):
            logging.debug("IsTrustedMemberHandler пропущен: from_user_id не установлен")
            return await super().handle(message)

        user_id = message.message.from_user_id
        joined_time = await self.__database_connection.get_member_joined_at(user_id)

        if joined_time is None:
            await self.__database_connection.add_member(user_id, time.time())
        elif joined_time + self.IS_TRUSTED_MEMBER < time.time():
            logging.info("IsTrustedMemberHandler worked now")
            return message

        return await super().handle(message)

    def is_available(self) -> bool:
        return self.__is_available
