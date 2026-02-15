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

        text = False
        caption = False
        if message.message.text is not None:
            if len(message.message.text.split(" ")) > 7:
                text = neural_client.check_message(message.message.text)

        if message.message.caption is not None:
            if len(message.message.caption.split(" ")) > 7:
                caption = neural_client.check_message(message.message.caption)

        if caption or text:
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("NeuralCheckHandler worked now")
            return message

        return await super().handle(message)
