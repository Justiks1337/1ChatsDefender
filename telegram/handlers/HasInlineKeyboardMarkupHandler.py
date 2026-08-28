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
        if not isinstance(message.message.reply_markup, bool):
            logging.debug("HasInlineKeyboardMarkupHandler пропущен: reply_markup не установлен")
            return await super().handle(message)

        # Проверяем наличие markup
        if not message.message.reply_markup:
            return await super().handle(message)

        message.is_trusted = False
        message.execute_middleware = True
        message.execute = ban(message.message)
        logging.debug("HasInlineKeyboardMarkupHandler is work now!")
        return message
