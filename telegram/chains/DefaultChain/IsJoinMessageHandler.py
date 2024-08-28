import aiogram.types

from utils import AbstractHandler
from telegram.Message import Message


class IsJoinMessageHandler(AbstractHandler):
    async def handle(self, message: Message) -> Message:
        if message.message.content_type == aiogram.types.ContentType.NEW_CHAT_MEMBERS:
            return message
        return await super().handle(message)
