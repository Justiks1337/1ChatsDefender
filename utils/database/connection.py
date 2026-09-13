from typing import Optional
import os

import aiosqlite
from dotenv import load_dotenv

from utils import Singleton


load_dotenv()


class DatabaseConnection(Singleton):
    def init(self):
        self.connect: Optional[aiosqlite.Connection] = None

    async def create_tables(self):
        async with self.connect.execute("""CREATE TABLE IF NOT EXISTS banned_messages (
            message TEXT PRIMARY KEY,
            payload TEXT
            )
        """):
            pass

        async with self.connect.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            warnings INTEGER
        )"""):
            pass

        async with self.connect.execute("""CREATE TABLE IF NOT EXISTS member_joins (
            user_id INTEGER PRIMARY KEY,
            joined_at INTEGER
        )"""):
            pass

        async with self.connect.execute("""CREATE TABLE IF NOT EXISTS trusted_messages (
            text TEXT,
            json_payload TEXT
        )"""):
            pass

        await self.connect.commit()

    async def get_connection(self):
        self.connect = await aiosqlite.connect(os.getenv("DATABASE_NAME"))
        await self.create_tables()

    async def is_message_banned(self, text: str) -> bool:
        async with self.connect.execute(
            "SELECT * FROM banned_messages WHERE message=?", (text,)
        ) as cursor:
            return await cursor.fetchone() is not None

    async def save_banned_message(self, text: Optional[str], payload: str):
        async with self.connect.execute(
            "INSERT OR IGNORE INTO banned_messages (message, payload) VALUES (?, ?)",
            (text, payload),
        ):
            pass
        await self.connect.commit()

    async def save_trusted_message(self, text: Optional[str], payload: str):
        async with self.connect.execute(
            "INSERT OR IGNORE INTO trusted_messages (text, json_payload) VALUES (?, ?)",
            (text, payload),
        ):
            pass
        await self.connect.commit()

    async def increment_warnings(self, user_id: int):
        async with self.connect.execute(
            """
            INSERT INTO users (user_id, warnings)
            VALUES (?, 1)
            ON CONFLICT(user_id) DO
            UPDATE SET warnings=warnings+1""",
            (user_id,),
        ):
            pass
        await self.connect.commit()

    async def has_reached_warning_limit(self, user_id: int, limit: int) -> bool:
        async with self.connect.execute(
            "SELECT user_id FROM users WHERE user_id = ? AND warnings >= ?",
            (user_id, limit),
        ) as cursor:
            return await cursor.fetchone() is not None

    async def get_member_joined_at(self, user_id: int) -> Optional[float]:
        async with self.connect.execute(
            "SELECT joined_at FROM member_joins WHERE user_id=?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
        return result[0] if result is not None else None

    async def add_member(self, user_id: int, joined_at: float):
        async with self.connect.execute(
            "INSERT INTO member_joins (user_id, joined_at) VALUES (?, ?)",
            (user_id, joined_at),
        ):
            pass
        await self.connect.commit()

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
