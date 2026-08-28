import logging

import aiogram.types

from utils import AbstractHandler
from telegram.Message import Message
from telegram.punishments import delete


class IsJoinMessageHandler(AbstractHandler):
    async def handle(self, message: Message) -> Message:
        if not isinstance(message.message.new_chat_members, bool):
            logging.debug("IsJoinMessageHandler пропущен: new_chat_members не установлен")
            return await super().handle(message)

        if message.message.new_chat_members:
            message.is_trusted = False
            message.execute = delete(message.message)
            logging.info("IsJoinMessageHandler is working now")
            return message

        return await super().handle(message)
