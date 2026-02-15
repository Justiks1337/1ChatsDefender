import os

from dotenv import load_dotenv

from telegram.Message import Message
from telegram.dispatcher import bot
from telegram.middleware.MiddlewareInterface import MiddlewareInterface

load_dotenv()


class SendMessageMiddleware(MiddlewareInterface):

    admins_chat_ids = int(os.getenv("ADMINS_CHAT_ID"))  # Save admin chat id

    @classmethod
    async def execute(cls, message: Message) -> Message:

        if message.message.text is None:
            return message

        message_to_admins_chat = os.getenv("VIOLATION_MESSAGE") \
            .replace("{nickname}", message.message.from_user.full_name) \
            .replace("{chat}", message.message.chat.title) \
            .replace("{message}", message.message.text)

        await bot.send_message(cls.admins_chat_ids, message_to_admins_chat)

        return message
