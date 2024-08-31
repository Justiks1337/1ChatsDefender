from telegram.middleware.MiddlewareInterface import MiddlewareInterface
from utils.database.connection import DatabaseConnection
from telegram.Message import Message


class MessageToDatabaseMiddleware(MiddlewareInterface):
    @classmethod
    async def execute(cls, message: Message) -> Message:
        if not message.is_trusted:
            connect = DatabaseConnection().connect
            await connect.execute("INSERT OR IGNORE INTO messages VALUES (?)", (message.message.text, ))
            await connect.commit()

        return message
