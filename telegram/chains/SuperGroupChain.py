import logging
import os

from utils import AbstractHandler
from telegram.Message import Message
from telegram.handlers.CheckInDatabaseHandler import CheckInDatabaseHandler
from telegram.handlers.NeuralCheckHandler import NeuralCheckHandler
from telegram.handlers.IsPremiumHandler import IsPremiumHandler
from telegram.handlers.HasPremiumEmojisHandler import HasPremiumEmojisHandler
from telegram.handlers.ManySpacesHandler import ManySpacesHandler
from telegram.handlers.CheckBanwordsHandler import CheckBanwordsHandler


class SuperGroupChain(AbstractHandler):

    whitelisted_chats = [-1001440778604, -1001375992358, -4288058510, -1002184712714, -4520083042, -1002168533309]

    async def handle(self, message: Message):

        if message.message.chat.id not in SuperGroupChain.whitelisted_chats:
            return await super().handle(message)

        check_in_database_handler = CheckInDatabaseHandler()
        neural_check_handler = NeuralCheckHandler()
        many_spaces_handler = ManySpacesHandler()
        has_premium_emojis_handler = HasPremiumEmojisHandler()
        is_premium_handler = IsPremiumHandler()
        ban_words_check_handler = CheckBanwordsHandler(text=os.getenv("SUPERGROUP_BANWORD_REGEX"))

        (
            is_premium_handler.set_next(has_premium_emojis_handler)
            .set_next(many_spaces_handler)
            .set_next(ban_words_check_handler)
            .set_next(check_in_database_handler)
            .set_next(neural_check_handler)
        )

        result = await is_premium_handler.handle(message)

        if not result.is_trusted or not result.next_handler:
            logging.info("SuperGroupChain handle a violation!")
            return message

        return await super().handle(message)
