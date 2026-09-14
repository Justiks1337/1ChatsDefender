import os
import logging

from dotenv import load_dotenv

from telegram.validate.Context import Context
from telegram.dispatcher import bot
from telegram.middleware.AbstractHandler import AbstractHandler

load_dotenv()


class SendMessageMiddleware(AbstractHandler):

    admins_chat_ids = int(os.environ["ADMINS_CHAT_ID"])  # Save admin chat id

    async def execute(self, context: Context) -> None:

        text = context.message.text
        if not isinstance(text, str):
            return

        template = os.getenv("VIOLATION_MESSAGE")
        if not template:
            logging.warning("Уведомление пропущено: VIOLATION_MESSAGE не задано")
            return

        nickname = context.message.from_user_full_name
        chat_title = context.message.chat_title
        if not isinstance(nickname, str):
            nickname = "Неизвестный отправитель"
        if not isinstance(chat_title, str):
            chat_title = "Чат без названия"

        message_to_admins_chat = template \
            .replace("{nickname}", nickname) \
            .replace("{chat}", chat_title) \
            .replace("{message}", text)

        await bot.send_message(self.admins_chat_ids, message_to_admins_chat)
