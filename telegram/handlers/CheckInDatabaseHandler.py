import logging

import aiosqlite

from utils import AbstractHandler
from telegram.Context import Context
from utils.database.connection import DatabaseConnection
from telegram.punishments import warning


class CheckInDatabaseHandler(AbstractHandler):
    async def handle(self, message: Context):
        if not isinstance(message.message.text, str):
            logging.debug("CheckInDatabaseHandler пропущен: text не установлен")
            return await super().handle(message)

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
