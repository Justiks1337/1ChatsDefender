import logging
import os

from telegram.validate.handlers import AbstractHandler
from telegram.validate.Context import Context
from telegram.validate.handlers import CheckInDatabaseHandler
from telegram.validate.handlers import NeuralCheckHandler
from telegram.validate.handlers import HasPremiumEmojisHandler
from telegram.validate.handlers import ManySpacesHandler
from telegram.validate.handlers import RegexHandler
from telegram.validate.handlers import HasInlineKeyboardMarkupHandler
from telegram.validate.handlers.IsTrustedMemberHandler import IsTrustedMemberHandler
from telegram.validate.handlers import UpperCaseHandler
from telegram.validate.handlers import EmptyHandler
from telegram.validate.handlers import StoryIsExistsHandler
from telegram.validate.handlers import ImageTextHandler
from telegram.validate.handlers import HasExternalReplyHandler


class SuperGroupChain(AbstractHandler):

    whitelisted_chats = [-1001440778604, -1001375992358, -4288058510, -1002184712714, -4520083042, -1002168533309, -1002590134862, -1002090117492]

    def __init__(self):
        self.first_handler = EmptyHandler()
        handlers = [
            HasInlineKeyboardMarkupHandler(),
            IsTrustedMemberHandler(),
            HasExternalReplyHandler(),
            HasPremiumEmojisHandler(),
            ManySpacesHandler(),
            UpperCaseHandler(),
            RegexHandler(text=os.getenv("SUPERGROUP_BANWORD_REGEX")),
            CheckInDatabaseHandler(),
            StoryIsExistsHandler(),
            NeuralCheckHandler(),
            ImageTextHandler(),
        ]

        current_handler = self.first_handler
        for handler in handlers:
            if handler.is_available():
                current_handler = current_handler.set_next(handler)

    async def handle(self, message: Context):
        if not isinstance(message.message.chat_id, int):
            logging.debug("SuperGroupChain пропущена: chat_id не установлен")
            return await super().handle(message)

        if message.message.chat_id not in SuperGroupChain.whitelisted_chats:
            return await super().handle(message)

        result: Context = await self.first_handler.handle(message)

        if result.punishment is not None or not result.next_handler:
            logging.info("SuperGroupChain handle a violation!")
            return message

        return await super().handle(message)

    def is_available(self) -> bool:
        return True
