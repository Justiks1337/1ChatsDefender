import json

from telegram.validate.sentinels import UnsetType

from telegram.middleware.AbstractHandler import AbstractHandler
from utils.database.connection import DatabaseConnection
from telegram.validate.Context import Context


class MessageToDatabaseMiddleware(AbstractHandler):
    """Сохраняет в БД сообщения, представляющие интерес для анализа.

    Записывает сообщения с назначенным наказанием: их текст или подпись
    и сериализованные данные. Признак is_trusted в контексте определяет,
    попадёт запись в таблицу доверенных или запрещённых сообщений.
    """
    async def execute(self, context: Context) -> None:

        if context.punishment is None:
            return

        database = DatabaseConnection()
        # для MessageData с учётом UNSET и вложенных объектов photo.
        payload = json.dumps(
            context.message.model_dump(), ensure_ascii=False, indent=4, default=str
        )
        text = context.message.text
        if text is None or isinstance(text, UnsetType):
            text = context.message.caption
        if isinstance(text, UnsetType):
            text = None
        if text is not None and not isinstance(text, str):
            raise TypeError("Текст для записи в БД должен быть строкой или None")
        if context.punishment is not None:
            await database.save_banned_message(text, payload)
        else:
            await database.save_trusted_message(text, payload)

    def __serialize_message(self):
        pass
