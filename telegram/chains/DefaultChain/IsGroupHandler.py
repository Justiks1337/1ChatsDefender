from telegram.Message import Message
from utils import AbstractHandler
from telegram.punishments import delete


class IsGroupHandler(AbstractHandler):
    """
    This handler check, message send in a group, or in a dm
    """
    async def handle(self, message: Message):
        if message.message.chat.id == message.message.from_user.id:
            message.is_trusted = False
            return message

        return await super().handle(message)
