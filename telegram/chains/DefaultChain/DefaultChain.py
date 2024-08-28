from utils import AbstractHandler
from telegram.Message import Message
from telegram.chains.DefaultChain.IsJoinMessageHandler import IsJoinMessageHandler
from telegram.chains.DefaultChain.IsAdminHandler import IsAdminHandler
from telegram.chains.DefaultChain.CheckBanwordsHandler import CheckBanwordsHandler


class DefaultChain(AbstractHandler):
    async def handle(self, message: Message):
        is_join_message_handler = IsJoinMessageHandler()
        is_admin_handler = IsAdminHandler()
        check_banwords_handler = CheckBanwordsHandler()

        is_join_message_handler.set_next(is_admin_handler).set_next(check_banwords_handler)

        result = await is_admin_handler.handle(message)

        if not result.is_trusted:
            return message

        return super().handle(message)
