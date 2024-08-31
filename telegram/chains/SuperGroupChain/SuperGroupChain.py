import logging

from utils import AbstractHandler
from telegram.Message import Message
from telegram.chains.SuperGroupChain.CheckInDatabaseHandler import CheckInDatabaseHandler
from telegram.chains.SuperGroupChain.NeuralCheckHandler import NeuralCheckHandler
from telegram.chains.SuperGroupChain.IsPremiumHandler import IsPremiumHandler


class SuperGroupChain(AbstractHandler):

    whitelisted_chats = [-1001375992358, -4288058510, -1002184712714, -4520083042, -1002168533309]

    async def handle(self, message: Message):

        if message.message.chat.id not in SuperGroupChain.whitelisted_chats:
            return await super().handle(message)

        check_in_database_handler = CheckInDatabaseHandler()
        neural_check_handler = NeuralCheckHandler()
        is_premium_handler = IsPremiumHandler()

        is_premium_handler.set_next(check_in_database_handler).set_next(neural_check_handler)

        result = await is_premium_handler.handle(message)

        if not result.is_trusted:
            logging.info("SuperGroupChain handle a violation!")
            return message

        return await super().handle(message)
