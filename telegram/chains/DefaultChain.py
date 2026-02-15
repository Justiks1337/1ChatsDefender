import logging

from utils import AbstractHandler
from telegram.Message import Message
from telegram.handlers.IsJoinMessageHandler import IsJoinMessageHandler
from telegram.handlers.IsAdminHandler import IsAdminHandler
from telegram.handlers.CheckBanwordsHandler import CheckBanwordsHandler
from telegram.handlers.IsGroupHandler import IsGroupHandler
from telegram.handlers.EmptyHandler import EmptyHandler


class DefaultChain(AbstractHandler):

    def __init__(self):
        self.first_handler = EmptyHandler()
        is_group_handler = IsGroupHandler()
        is_join_message_handler = IsJoinMessageHandler()
        is_admin_handler = IsAdminHandler()
        check_banwords_handler = CheckBanwordsHandler()

        (
            self.first_handler
            .set_next(is_group_handler)
            .set_next(is_join_message_handler)
            .set_next(is_admin_handler)
            .set_next(check_banwords_handler)
        )

    async def handle(self, message: Message):
        result = await self.first_handler.handle(message)

        if not result.is_trusted or not result.next_handler:
            logging.info("Default chain handle a violation.")
            return result

        return await super().handle(message)
