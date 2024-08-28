from utils import AbstractHandler
from telegram.Message import Message
from telegram.chains.SuperGroupChain.CheckInDatabaseHandler import CheckInDatabaseHandler
from telegram.chains.SuperGroupChain.NeuralCheckHandler import NeuralCheckHandler


class SuperGroupChain(AbstractHandler):
    async def handle(self, message: Message):

        # TODO: check whitelist

        check_in_database_handler = CheckInDatabaseHandler()
        neural_check_handler = NeuralCheckHandler()

        check_in_database_handler.set_next(neural_check_handler)

        result = await check_in_database_handler.handle(message)

        if result.is_trusted:
            return message

        return await super().handle(message)
