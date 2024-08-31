from telegram.Message import Message
from utils import AbstractHandler


class MessageHasTextHandler(AbstractHandler):
    """
    Message text can be is None, for ex., if message is photo without caption, or message is voice message.
    Further validate message is senselessly, because my algorithm can't moderate this messages.
                                                                                    """

    async def handle(self, message: Message) -> Message:
        if not message.message.text:
            message.is_trusted = False
            return message

        return await super().handle(message)
