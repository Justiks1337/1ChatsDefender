import logging

import emoji

from telegram.validate.handlers import AbstractHandler
from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType


# TODO: rewrite with message entities
class HasPremiumEmojisHandler(AbstractHandler):
    def _check_message(self, text: object, caption: object) -> bool:
        return not (self._validate_text(text) and self._validate_text(caption))

    async def handle(self, message: Context):
        text = message.message.text
        caption = message.message.caption
        if not isinstance(text, str) and not isinstance(caption, str):
            logging.debug("HasPremiumEmojisHandler пропущен: text и caption не установлены")
            return await super().handle(message)

        if self._check_message(text, caption):
            message.is_trusted = False
            message.execute_middleware = True
            message.punishment = PunishmentCommand(
                PunishmentType.WARNING,
                reason="Превышен лимит эмодзи",
                source=type(self).__name__,
            )
            logging.info("HasPremiumEmojisHandler is worked now")
            return message

        return await super().handle(message)

    def _validate_text(self, text: object) -> bool:
        result = 0

        if not isinstance(text, str):
            return True

        for symbol in text:
            if emoji.is_emoji(symbol):  # check symbol is emoji
                result += 1

                if result > 4:  # 5 - message limit of emojis. If amount of emojis = 5 - message is not trusted
                    return False

        return True

    def is_available(self) -> bool:
        return True
