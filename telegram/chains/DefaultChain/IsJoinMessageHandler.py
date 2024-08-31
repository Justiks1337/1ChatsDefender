import aiogram.types

from utils import AbstractHandler
from telegram.Message import Message
from telegram.punishments import delete


class IsJoinMessageHandler(AbstractHandler):
    async def handle(self, message: Message) -> Message:
        if message.message.new_chat_members:
            message.is_trusted = False
            message.execute = delete(message.message)
            return message

        return await super().handle(message)
