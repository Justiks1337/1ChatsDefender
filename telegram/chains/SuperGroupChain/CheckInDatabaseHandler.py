import logging

import aiosqlite

from utils import AbstractHandler
from telegram.Message import Message
from utils.database.connection import DatabaseConnection
from telegram.punishments import warning


class CheckInDatabaseHandler(AbstractHandler):
    async def handle(self, message: Message):
        cursor: aiosqlite.Cursor = await DatabaseConnection().connect.cursor()
        result_set = await cursor.execute(
            "SELECT * FROM messages WHERE message=?",
            (message.message.text, ))

        if await result_set.fetchone():
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("CheckInDatabaseHandler is worked now")
            return message

        return await super().handle(message)
