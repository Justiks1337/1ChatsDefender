import logging

import emoji

from utils import AbstractHandler
from telegram.Message import Message
from telegram.punishments import warning


# TODO: rewrite with message entities
class HasPremiumEmojisHandler(AbstractHandler):
    async def handle(self, message: Message):

        if not (self.validate_text(message.message.text) and self.validate_text(
                message.message.caption)):  # 5 - message limit of emojis. If amount of emojis = 5 - message is not trusted
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("HasPremiumEmojisHandler is worked now")
            return message

        return await super().handle(message)

    def validate_text(self, text: str | None):
        result = 0

        if text is None:
            return True

        for symbol in text:
            if emoji.is_emoji(symbol):  # check symbol is emoji
                result += 1

                if result > 4:  # 5 - message limit of emojis. If amount of emojis = 5 - message is not trusted
                    return False

        return True
