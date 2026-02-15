import logging
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
        await self.connect.execute("""CREATE TABLE IF NOT EXISTS banned_messages (
            message TEXT PRIMARY KEY,
            payload TEXT
            )
        """)

        await self.connect.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            warnings INTEGER
        )""")

        await self.connect.execute("""CREATE TABLE IF NOT EXISTS member_joins (
            user_id INTEGER PRIMARY KEY,
            joined_at INTEGER
        )""")

        await self.connect.execute("""CREATE TABLE IF NOT EXISTS trusted_messages (
            text TEXT,
            json_payload TEXT
        )""")

        await self.connect.commit()

    async def get_connection(self):
        self.connect = await aiosqlite.connect(os.getenv("DATABASE_NAME"))
        await self.create_tables()
