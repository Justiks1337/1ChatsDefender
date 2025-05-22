import logging

from telegram.admin_management import ChatAdminsFabric
from utils import AbstractHandler

from telegram.Message import Message


class IsAdminHandler(AbstractHandler):

    async def handle(self, message: Message) -> Message:
        if await ChatAdminsFabric().is_admin(message.message):
            logging.debug("IsAdminHandler is worked now")
            message.next_handler = False
            return message
        return await super().handle(message)
