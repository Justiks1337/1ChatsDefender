import logging

from telegram.admin_management import ChatAdminsFabric
from utils import AbstractHandler

from telegram.Context import Context


class IsAdminHandler(AbstractHandler):

    async def handle(self, message: Context) -> Context:
        if not isinstance(message.message.chat_id, int) or not isinstance(message.message.from_user_id, int):
            logging.debug("IsAdminHandler пропущен: chat_id или from_user_id не установлен")
            return await super().handle(message)

        if await ChatAdminsFabric().is_admin(message.message):
            logging.debug("IsAdminHandler is worked now")
            message.next_handler = False
            return message
        return await super().handle(message)
