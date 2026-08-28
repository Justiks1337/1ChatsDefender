"""This coroutines uses in Executor"""
import os
import logging

import aiogram.exceptions
import aiogram.types
from dotenv import load_dotenv

from telegram.dispatcher import bot
from utils.database.connection import DatabaseConnection

load_dotenv()

MAX_WARNINGS = int(os.getenv("MAX_WARNINGS"))  # Used in warnings async function


async def delete(message: aiogram.types.Message):
    """
    punishment, use in all other punishments, and can be used directly

    :param message: aiogram.types.Message, "canceled" message
    :return:
    """

    await bot.delete_message(message.chat_id, message.message_id)
    logging.debug(f"message <{message.text}> in {message.chat_title} was deleted")


async def warning(message: aiogram.types.Message):
    database_connection = DatabaseConnection().connect

    await database_connection.execute("""
            INSERT INTO users (user_id, warnings)
            VALUES (?, 1)
            ON CONFLICT(user_id) DO
            UPDATE SET warnings=warnings+1""", (
        message.from_user_id,
    ))

    await database_connection.commit()

    result_set = await database_connection.execute(
        "SELECT user_id FROM users WHERE user_id = ? AND warnings >= ? ", (
            message.from_user_id,
            MAX_WARNINGS))

    if await result_set.fetchone():
        await ban(message)
        return

    await delete(message)


async def ban(message: aiogram.types.Message):
    await delete(message)
    try:
        await bot.ban_chat_member(message.chat_id, message.from_user_id)
        logging.info(f"user {message.from_user_full_name} banned in {message.chat_title}")
    except aiogram.exceptions.TelegramBadRequest:
        logging.warning(
            f"user {message.from_user_id} could be banned, but bot has no access to ban in group {message.chat_id}"
        )
