import logging

from telegram.Message import Message
from telegram.punishments import ban
from utils.patterns.chain_of_responsibility import AbstractHandler


class HasInlineKeyboardMarkupHandler(AbstractHandler):
    """
    В чат отправляются сообщения с кнопками, созданными при помощи ботов и телеграмм-каналов.
    Этот хандлер удаляет подобные сообщения
    """

    async def handle(self, message: Message):
        # Проверяем наличие markup
        if message.message.reply_markup is None:
            return await super().handle(message)

        message.is_trusted = False
        message.execute_middleware = True
        message.execute = ban(message)
        logging.debug("HasInlineKeyboardMarkupHandler is work now!")
        return message