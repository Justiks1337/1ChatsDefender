import os
import logging

from dotenv import load_dotenv

from telegram.validate.Context import Context
from telegram.dispatcher import bot
from telegram.middleware.MiddlewareInterface import MiddlewareInterface

load_dotenv()


class SendMessageMiddleware(MiddlewareInterface):

    admins_chat_ids = int(os.environ["ADMINS_CHAT_ID"])  # Save admin chat id

    @classmethod
    async def execute(cls, message: Context) -> Context:

        text = message.message.text
        if not isinstance(text, str):
            return message

        template = os.getenv("VIOLATION_MESSAGE")
        if not template:
            logging.warning("Уведомление пропущено: VIOLATION_MESSAGE не задано")
            return message

        nickname = message.message.from_user_full_name
        chat_title = message.message.chat_title
        if not isinstance(nickname, str):
            nickname = "Неизвестный отправитель"
        if not isinstance(chat_title, str):
            chat_title = "Чат без названия"

        message_to_admins_chat = template \
            .replace("{nickname}", nickname) \
            .replace("{chat}", chat_title) \
            .replace("{message}", text)

        await bot.send_message(cls.admins_chat_ids, message_to_admins_chat)

        return message
