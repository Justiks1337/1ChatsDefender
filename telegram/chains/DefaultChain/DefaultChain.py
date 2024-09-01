import logging

from utils import AbstractHandler
from telegram.Message import Message
from telegram.chains.DefaultChain.IsJoinMessageHandler import IsJoinMessageHandler
from telegram.chains.DefaultChain.IsAdminHandler import IsAdminHandler
from telegram.chains.DefaultChain.CheckBanwordsHandler import CheckBanwordsHandler
from telegram.chains.DefaultChain.MessageHasTextHandler import MessageHasTextHandler
from telegram.chains.DefaultChain.IsGroupHandler import IsGroupHandler


class DefaultChain(AbstractHandler):
    async def handle(self, message: Message):
        is_group_handler = IsGroupHandler()
        is_join_message_handler = IsJoinMessageHandler()
        message_has_text_handler = MessageHasTextHandler()
        is_admin_handler = IsAdminHandler()
        check_banwords_handler = CheckBanwordsHandler()

        is_group_handler.set_next(is_join_message_handler).set_next(message_has_text_handler).set_next(is_admin_handler).set_next(check_banwords_handler)

        result = await is_join_message_handler.handle(message)

        if not result.is_trusted:
            logging.info("Default chain handle a violation.")
            return result

        return await super().handle(message)
