import logging

import emoji

from utils import AbstractHandler
from telegram.Message import Message
from telegram.punishments import warning


# TODO: rewrite with message entities
class HasPremiumEmojisHandler(AbstractHandler):
    async def handle(self, message: Message):
        text = message.message.text
        caption = message.message.caption
        if not isinstance(text, str) and not isinstance(caption, str):
            logging.debug("HasPremiumEmojisHandler пропущен: text и caption не установлены")
            return await super().handle(message)

        if not (self.validate_text(text) and self.validate_text(
                caption)):  # 5 - message limit of emojis. If amount of emojis = 5 - message is not trusted
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("HasPremiumEmojisHandler is worked now")
            return message

        return await super().handle(message)

    def validate_text(self, text: object):
        result = 0

        if not isinstance(text, str):
            return True

        for symbol in text:
            if emoji.is_emoji(symbol):  # check symbol is emoji
                result += 1

                if result > 4:  # 5 - message limit of emojis. If amount of emojis = 5 - message is not trusted
                    return False

        return True
