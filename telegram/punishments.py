"""This coroutines uses in Executor"""

import aiogram.types
import aiogram.exceptions

from telegram.dispatcher import bot
from utils.database.connection import DatabaseConnection


async def delete(message: aiogram.types.Message):
    """
    punishment, use in all other punishments, and can be used directly

    :param message: aiogram.types.Message, "canceled" message
    :return:
    """

    await bot.delete_message(message.chat.id, message.message_id)


async def warning(message: aiogram.types.Message):

    # TODO: ban after 3 warnings

    database_connection = DatabaseConnection().connect

    await database_connection.execute(
        "INSERT INTO users VALUES (?, 1) ON CONFLICT(user_id) DO UPDATE SET warnings=warnings+1",
        (message.from_user.id, ))

    await delete(message)


async def ban(message: aiogram.types.Message):
    await delete(message)
    try:
        await bot.ban_chat_member(message.chat.id, message.from_user.id)
    except aiogram.exceptions.TelegramBadRequest:
        print(f"user {message.from_user.id} could be banned, but bot has no access to ban in group {message.chat.id}")
