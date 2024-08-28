"""This coroutines uses in Executor"""

import aiogram.types

from telegram.dispatcher import bot
from utils.database.connection import DatabaseConnection


async def __delete(message: aiogram.types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


async def warning(message: aiogram.types.Message):
    database_connection = DatabaseConnection().connect

    await database_connection.execute(
        "INSERT INTO users * VALUES (?, 1) ON CONFLICT(user_id) DO UPDATE SET warnings=warnings+1",
        (message.from_user.id, ))

    await __delete(message)


async def ban(message: aiogram.types.Message):
    await __delete(message)
    await bot.ban_chat_member(message.chat.id, message.from_user.id)
