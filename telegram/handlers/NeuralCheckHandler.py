import logging

from dotenv import load_dotenv

from telegram.Context import Context
from telegram.punishments import warning
from utils import AbstractHandler
from utils.AIClient import AIClient

load_dotenv()


class NeuralCheckHandler(AbstractHandler):

    async def handle(self, message: Context):
        message_text = message.message.text
        message_caption = message.message.caption
        if not isinstance(message_text, str) and not isinstance(message_caption, str):
            logging.debug("NeuralCheckHandler пропущен: text и caption не установлены")
            return await super().handle(message)

        neural_client = AIClient()

        text = False
        caption = False
        if isinstance(message_text, str):
            if len(message_text.split(" ")) > 7:
                text = neural_client.check_message(message_text)

        if isinstance(message_caption, str):
            if len(message_caption.split(" ")) > 7:
                caption = neural_client.check_message(message_caption)

        if caption or text:
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("NeuralCheckHandler worked now")
            return message

        return await super().handle(message)
