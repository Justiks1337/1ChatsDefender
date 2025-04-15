import time
import os
from typing import Optional

from telegram.Message import Message
from utils.patterns.chain_of_responsibility import AbstractHandler
from utils.database.connection import DatabaseConnection


class IsTrustedMemberHandler(AbstractHandler):
    """
    Проверка, является ли пользователь доверенным
    Пользователем является доверенным если он находится в чатах более IS_TRUSTED_MEMBER секунд
    """

    # Время в секундах, после которого пользователь считается доверенным и игнорируется
    IS_TRUSTED_MEMBER = int(os.getenv('IS_TRUSTED_MEMBER'))

    async def handle(self, message: Message):
        user_id = message.message.from_user.id
        joined_time: int = await self.__get_joined_time(user_id)

        if joined_time is None:
            await self.__add_new_member(user_id)
        if joined_time + self.IS_TRUSTED_MEMBER < time.time():
            return message

        return await super().handle(message)

    async def __get_joined_time(self, user_id: int) -> Optional[int]:
        """
        Верните время входа пользователя в чат, или верните None
        :param user_id: Айди пользователя
        :return: Время входа пользователя или None
        """

        cursor = await DatabaseConnection().connect.execute(
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

        await DatabaseConnection().connect.execute(
            "INSERT INTO member_joins VALUES (?, ?)", (
                user_id,
                time.time())
        )
