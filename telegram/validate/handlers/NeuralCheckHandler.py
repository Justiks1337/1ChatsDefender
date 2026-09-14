import logging

from telegram.validate.Context import Context
from telegram.validate.handlers import AbstractHandler
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType


class NeuralCheckHandler(AbstractHandler):

    def __init__(self):
        self.__is_available = True

        try:
            from utils.AIClient import AIClient
            self.__ai_client = AIClient()
        except ImportError:
            self.__is_available = False
            logging.error(
                "Не удалось загрузить NeuralCheckHandler из-за недостающей зависимости"
            )

    def _check_message(self, text: object, caption: object) -> bool:
        neural_client = self.__ai_client
        text_result = False
        caption_result = False

        if isinstance(text, str) and len(text.split()) > 7:
            text_result = neural_client.check_message(text)
        if isinstance(caption, str) and len(caption.split()) > 7:
            caption_result = neural_client.check_message(caption)

        return caption_result or text_result

    async def handle(self, message: Context):
        message_text = message.message.text
        message_caption = message.message.caption
        if not isinstance(message_text, str) and not isinstance(message_caption, str):
            logging.debug("NeuralCheckHandler пропущен: text и caption не установлены")
            return await super().handle(message)

        if self._check_message(message_text, message_caption):
            message.punishment = PunishmentCommand(
                PunishmentType.WARNING,
                reason="Сообщение отклонено моделью",
                source=type(self).__name__,
            )
            logging.info("NeuralCheckHandler worked now")
            return message

        return await super().handle(message)

    def is_available(self) -> bool:
        return self.__is_available
