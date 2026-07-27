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
from telegram.handlers.HasInlineKeyboardMarkupHandler import HasInlineKeyboardMarkupHandler
from telegram.handlers.IsTrustedMemberHandler import IsTrustedMemberHandler
from telegram.handlers.UpperCaseHandler import UpperCaseHandler
from telegram.handlers.EmptyHandler import EmptyHandler
from telegram.handlers.StoryIsExistsHandler import StoryIsExistsHandler
from telegram.handlers.ImageTextHandler import ImageTextHandler
from telegram.handlers.HasExternalReplyHandler import HasExternalReplyHandler


class SuperGroupChain(AbstractHandler):

    whitelisted_chats = [-1001440778604, -1001375992358, -4288058510, -1002184712714, -4520083042, -1002168533309, -1002590134862, -1002090117492]

    def __init__(self):
        self.first_handler = EmptyHandler()
        check_in_database_handler = CheckInDatabaseHandler()
        neural_check_handler = NeuralCheckHandler()
        many_spaces_handler = ManySpacesHandler()
        has_premium_emojis_handler = HasPremiumEmojisHandler()
        is_premium_handler = IsPremiumHandler()
        ban_words_check_handler = CheckBanwordsHandler(text=os.getenv("SUPERGROUP_BANWORD_REGEX"))
        has_inline_keyboard_markup = HasInlineKeyboardMarkupHandler()
        is_trusted_member_handler = IsTrustedMemberHandler()
        is_uppercase_handler = UpperCaseHandler()
        story_is_exists_handler = StoryIsExistsHandler()
        image_text_handler = ImageTextHandler()
        has_external_reply_handler = HasExternalReplyHandler()

        (
            self.first_handler
            .set_next(has_inline_keyboard_markup)
            .set_next(is_trusted_member_handler)
            .set_next(has_external_reply_handler)
            .set_next(has_premium_emojis_handler)
            .set_next(many_spaces_handler)
            .set_next(is_uppercase_handler)
            .set_next(ban_words_check_handler)
            .set_next(is_premium_handler)
            .set_next(check_in_database_handler)
            .set_next(story_is_exists_handler)
            .set_next(neural_check_handler)
            .set_next(image_text_handler)
        )

    async def handle(self, message: Message):

        if message.message.chat.id not in SuperGroupChain.whitelisted_chats:
            return await super().handle(message)

        result = await self.first_handler.handle(message)

        if not result.is_trusted or not result.next_handler:
            logging.info("SuperGroupChain handle a violation!")
            return message

        return await super().handle(message)
