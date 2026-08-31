import time
import os
from typing import Optional
import logging

from telegram.validate.Context import Context
from telegram.validate.handlers.AbstractHandler import AbstractHandler


class IsTrustedMemberHandler(AbstractHandler):
    """
    Проверка, является ли пользователь доверенным
    Пользователем является доверенным если он находится в чатах более IS_TRUSTED_MEMBER секунд
    """

    # Время в секундах, после которого пользователь считается доверенным и игнорируется
    IS_TRUSTED_MEMBER = int(os.getenv('IS_TRUSTED_MEMBER'))

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
        joined_time: int = await self.__get_joined_time(user_id)

        if joined_time is None:
            await self.__add_new_member(user_id)
        elif joined_time + self.IS_TRUSTED_MEMBER < time.time():
            logging.info("IsTrustedMemberHandler worked now")
            return message

        return await super().handle(message)

    async def __get_joined_time(self, user_id: int) -> Optional[int]:
        """
        Верните время входа пользователя в чат, или верните None
        :param user_id: Айди пользователя
        :return: Время входа пользователя или None
        """

        cursor = await self.__database_connection.connect.execute(
            "SELECT joined_at FROM member_joins WHERE user_id=?", (
                user_id,)
        )

        result = await cursor.fetchone()

        if result is None:
            return None

        return result[0]

    async def __add_new_member(self, user_id: int):
        """
        Добавь нового участника в базу
        :param user_id: id участника
        :return: None
        """

        await self.__database_connection.connect.execute(
            "INSERT INTO member_joins VALUES (?, ?)", (
                user_id,
                time.time())
        )

    def is_available(self) -> bool:
        return self.__is_available
