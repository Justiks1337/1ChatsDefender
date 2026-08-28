import os

from dotenv import load_dotenv

from telegram.Context import Context
from telegram.dispatcher import bot
from telegram.middleware.MiddlewareInterface import MiddlewareInterface

load_dotenv()


class SendMessageMiddleware(MiddlewareInterface):

    admins_chat_ids = int(os.getenv("ADMINS_CHAT_ID"))  # Save admin chat id

    @classmethod
    async def execute(cls, message: Context) -> Context:

        if message.message.text is None:
            return message

        message_to_admins_chat = os.getenv("VIOLATION_MESSAGE") \
            .replace("{nickname}", message.message.from_user_full_name) \
            .replace("{chat}", message.message.chat_title) \
            .replace("{message}", message.message.text)

        await bot.send_message(cls.admins_chat_ids, message_to_admins_chat)

        return message
