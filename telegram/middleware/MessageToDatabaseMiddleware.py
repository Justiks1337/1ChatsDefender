import json

from telegram.validate.sentinels import UnsetType

from telegram.middleware.MiddlewareInterface import MiddlewareInterface
from utils.database.connection import DatabaseConnection
from aiogram.utils.serialization import deserialize_telegram_object_to_python
from telegram.validate.Context import Context


class MessageToDatabaseMiddleware(MiddlewareInterface):
    @classmethod
    async def execute(cls, message: Context) -> Context:
        database = DatabaseConnection()
        # TODO: Исправить использование deserialize_telegram_object_to_python
        # для MessageData с учётом UNSET и вложенных объектов photo.
        payload = json.dumps(
            deserialize_telegram_object_to_python(message.message), ensure_ascii=False, indent=4, default=str
        )
        text = message.message.text
        if isinstance(text, UnsetType):
            text = None
        if text is not None and not isinstance(text, str):
            raise TypeError("Текст для записи в БД должен быть строкой или None")
        if not message.is_trusted:
            await database.save_banned_message(text, payload)
        else:
            await database.save_trusted_message(text, payload)

        return message
