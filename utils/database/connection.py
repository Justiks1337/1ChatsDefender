from typing import Optional
import os

import aiosqlite
from dotenv import load_dotenv

from utils import Singleton


load_dotenv()


class DatabaseConnection(Singleton):
    """Обеспечивает взаимодействие с БД через единственный экземпляр.

    Использует паттерн Singleton. Инициализируйте объект и откройте соединение
    через get_connection перед запуском основной обработки сообщений.
    При завершении приложения закройте соединение методом close.

    Все операции взаимодействия с базой данных должны быть реализованы
    исключительно в этом классе. Он хранит запрещённые и доверенные
    сообщения, предупреждения и время регистрации участников.
    """

    def init(self):
        self.connect: Optional[aiosqlite.Connection] = None

    @property
    def connection(self) -> aiosqlite.Connection:
        connection = self.connect
        if connection is None:
            raise RuntimeError("Соединение с БД не открыто или уже закрыто")
        return connection

    async def create_tables(self):
        async with self.connection.execute("""CREATE TABLE IF NOT EXISTS banned_messages (
            message TEXT PRIMARY KEY,
            payload TEXT
            )
        """):
            pass

        async with self.connection.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            warnings INTEGER
        )"""):
            pass

        async with self.connection.execute("""CREATE TABLE IF NOT EXISTS member_joins (
            user_id INTEGER PRIMARY KEY,
            joined_at INTEGER
        )"""):
            pass

        async with self.connection.execute("""CREATE TABLE IF NOT EXISTS trusted_messages (
            text TEXT,
            json_payload TEXT
        )"""):
            pass

        await self.connection.commit()

    async def get_connection(self):
        self.connect = await aiosqlite.connect(os.environ["DATABASE_NAME"])
        await self.create_tables()

    async def is_message_banned(self, text: str) -> bool:
        async with self.connection.execute(
            "SELECT * FROM banned_messages WHERE message=?", (text,)
        ) as cursor:
            return await cursor.fetchone() is not None

    async def save_banned_message(self, text: Optional[str], payload: str):
        async with self.connection.execute(
            "INSERT OR IGNORE INTO banned_messages (message, payload) VALUES (?, ?)",
            (text, payload),
        ):
            pass
        await self.connection.commit()

    async def save_trusted_message(self, text: Optional[str], payload: str):
        async with self.connection.execute(
            "INSERT OR IGNORE INTO trusted_messages (text, json_payload) VALUES (?, ?)",
            (text, payload),
        ):
            pass
        await self.connection.commit()

    async def increment_warnings(self, user_id: int):
        async with self.connection.execute(
            """
            INSERT INTO users (user_id, warnings)
            VALUES (?, 1)
            ON CONFLICT(user_id) DO
            UPDATE SET warnings=warnings+1""",
            (user_id,),
        ):
            pass
        await self.connection.commit()

    async def has_reached_warning_limit(self, user_id: int, limit: int) -> bool:
        async with self.connection.execute(
            "SELECT user_id FROM users WHERE user_id = ? AND warnings >= ?",
            (user_id, limit),
        ) as cursor:
            return await cursor.fetchone() is not None

    async def get_member_joined_at(self, user_id: int) -> Optional[float]:
        async with self.connection.execute(
            "SELECT joined_at FROM member_joins WHERE user_id=?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
        if result is None or result[0] is None:
            return None
        joined_at = result[0]
        if type(joined_at) not in (int, float):
            raise TypeError("Время вступления в БД должно быть числом")
        return float(joined_at)

    async def add_member(self, user_id: int, joined_at: float):
        async with self.connection.execute(
            "INSERT INTO member_joins (user_id, joined_at) VALUES (?, ?)",
            (user_id, joined_at),
        ):
            pass
        await self.connection.commit()

    async def close(self):
        """
        Закрытие сессии aiosqlite
        Так как сессия открывается один раз при запуске бота, она никогда не закрывается
        Из-за этого процесс нужно очень неаккуратно убивать.

        Это плохая практика, поэтому вызывайте это перед завершением процесса
        :return: None
        """

        if self.connect is not None:
            await self.connect.close()
            self.connect = None
