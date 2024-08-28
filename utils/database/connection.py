from typing import Optional
import os

import aiosqlite3
from dotenv import load_dotenv

from utils import Singleton


load_dotenv()


class DatabaseConnection(Singleton):
    def init(self):
        self.connect: Optional[aiosqlite3.Connection] = None
        self.create_tables()

    async def create_tables(self):
        await self.connect.cursor().execute("""CREATE TABLE IF NOT EXISTS messages (
            message TEXT PRIMARY KEY
            )
        """)

        await self.connect.cursor().execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            warnings INTEGER
        )""")

    async def get_connection(self):
        self.connect = await aiosqlite3.connect(os.getenv("DATABASE_NAME"))
        await self.create_tables()
