import logging

import emoji

from utils import AbstractHandler
from telegram.Message import Message
from telegram.punishments import warning


class HasPremiumEmojisHandler(AbstractHandler):
    async def handle(self, message: Message):

        result = 0

        for symbol in message.message.text:
            if emoji.is_emoji(symbol):  # check symbol is emoji
                result += 1

                if result > 4:  # 5 - message limit of emojis. If amount of emojis = 5 - message is not trusted
                    message.is_trusted = False
                    message.execute_middleware = True
                    message.execute = warning(message.message)
                    logging.info("HasPremiumEmojisHandler is worked now")
                    return message

        return await super().handle(message)
