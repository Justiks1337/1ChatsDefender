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
        await self.connect.execute("""CREATE TABLE IF NOT EXISTS messages (
            message TEXT PRIMARY KEY
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

        logging.warning("starting add columns to messages table...")

        try:
            await self.connect.execute("""ALTER TABLE messages ADD COLUMN user_id INTEGER""")
            await self.connect.execute("""ALTER TABLE messages ADD COLUMN time INTEGER""")
            await self.connect.execute("""ALTER TABLE messages ADD COLUMN full_name TEXT""")
            await self.connect.execute("""ALTER TABLE messages ADD COLUMN username TEXT""")
            await self.connect.execute("""ALTER TABLE messages ADD COLUMN language_code TEXT""")
            await self.connect.execute("""ALTER TABLE messages ADD COLUMN is_premium INTEGER""")
            await self.connect.execute("""ALTER TABLE messages ADD COLUMN is_forwarded_message INTEGER""")
            await self.connect.execute("""ALTER TABLE messages ADD COLUMN is_reply INTEGER""")
            logging.warning("finished add columns to messages table!")
        except Exception as e:
            logging.critical("Columns now created, remove this!", e)

    async def get_connection(self):
        self.connect = await aiosqlite.connect(os.getenv("DATABASE_NAME"))
        await self.create_tables()
