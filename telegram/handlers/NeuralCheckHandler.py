import logging

from dotenv import load_dotenv

from telegram.Message import Message
from telegram.punishments import warning
from utils import AbstractHandler
from utils.AIClient import AIClient

load_dotenv()


class NeuralCheckHandler(AbstractHandler):

    async def handle(self, message: Message):
        neural_client = AIClient()

        # Я не хочу тратить токены в нейронке на маленькие сообщения. И писать отдельный хендлер под это не хочу. И вообще комментарий переводить на английский тоже лень
        if len(message.message.text.split(" ")) < 7:
            logging.debug("NeuralCheckHandler ignore message, because it len < 10")
            return await super().handle(message)

        if neural_client.check_message(message.message.text):
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("NeuralCheckHandler worked now")
            return message

        return await super().handle(message)
