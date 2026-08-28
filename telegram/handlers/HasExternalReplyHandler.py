import logging

from telegram.Message import Message
from telegram.punishments import ban
from utils import AbstractHandler


class HasExternalReplyHandler(AbstractHandler):
    async def handle(self, message: Message):
        if not isinstance(message.message.external_reply, bool):
            logging.debug("HasExternalReplyHandler пропущен: external_reply не установлен")
            return await super().handle(message)

        # Проверяем, есть ли external_reply в сообщении
        if message.message.external_reply:
            # Если есть external_reply, то автор сообщения должен быть забанен
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = ban(message.message)
            logging.info("HasExternalReplyHandler worked - user banned for external reply")
            return message

        # Если external_reply отсутствует, продолжаем цепочку
        return await super().handle(message)
