import json

from telegram.middleware.MiddlewareInterface import MiddlewareInterface
from utils.database.connection import DatabaseConnection
from aiogram.utils.serialization import deserialize_telegram_object_to_python
from telegram.validate.Context import Context


class MessageToDatabaseMiddleware(MiddlewareInterface):
    @classmethod
    async def execute(cls, message: Context) -> Context:
        database = DatabaseConnection()
        payload = json.dumps(
            deserialize_telegram_object_to_python(message.message), ensure_ascii=False, indent=4, default=str
        )
        if not message.is_trusted:
            await database.save_banned_message(message.message.text, payload)
        else:
            await database.save_trusted_message(message.message.text, payload)

        return message
