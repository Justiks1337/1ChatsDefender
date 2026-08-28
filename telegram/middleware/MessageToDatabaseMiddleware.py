import json

from telegram.middleware.MiddlewareInterface import MiddlewareInterface
from utils.database.connection import DatabaseConnection
from aiogram.utils.serialization import deserialize_telegram_object_to_python
from telegram.Context import Context


class MessageToDatabaseMiddleware(MiddlewareInterface):
    @classmethod
    async def execute(cls, message: Context) -> Context:
        connect = DatabaseConnection().connect
        if not message.is_trusted:
            await connect.execute("INSERT OR IGNORE INTO banned_messages VALUES (?, ?)", (
                message.message.text,
                json.dumps(deserialize_telegram_object_to_python(message.message), ensure_ascii=False, indent=4, default=str)
            ))

        else:
            await connect.execute("INSERT OR IGNORE INTO trusted_messages VALUES (?, ?)", (
                message.message.text,
                json.dumps(deserialize_telegram_object_to_python(message.message), ensure_ascii=False, indent=4, default=str)
            ))

        await connect.commit()

        return message
