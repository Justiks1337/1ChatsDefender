"""This coroutines uses in Executor"""
import os
import logging

import aiogram.exceptions
from dotenv import load_dotenv

from telegram.dispatcher import bot
from utils.database.connection import DatabaseConnection
from telegram.validate.MessageData import MessageData

load_dotenv()



MAX_WARNINGS = int(os.environ["MAX_WARNINGS"])  # Used in warnings async function


async def delete(message: MessageData):
    """
    punishment, use in all other punishments, and can be used directly

    :param message: aiogram.types.Message, "canceled" message
    :return:
    """

    if type(message.chat_id) is not int or type(message.message_id) is not int:
        raise TypeError("Для удаления нужны целочисленные chat_id и message_id")

    await bot.delete_message(message.chat_id, message.message_id)
    logging.debug(f"message <{message.text}> in {message.chat_title} was deleted")


async def warning(message: MessageData):
    database_connection = DatabaseConnection()

    if any(type(value) is not int for value in (
        message.chat_id, message.message_id, message.from_user_id
    )):
        raise TypeError("Для предупреждения нужны целочисленные chat_id, message_id и from_user_id")

    await database_connection.increment_warnings(message.from_user_id)

    if await database_connection.has_reached_warning_limit(message.from_user_id, MAX_WARNINGS):
        await ban(message)
        return

    await delete(message)


async def ban(message: MessageData):
    if any(type(value) is not int for value in (
        message.chat_id, message.message_id, message.from_user_id
    )):
        raise TypeError("Для бана нужны целочисленные chat_id, message_id и from_user_id")

    await delete(message)
    try:
        await bot.ban_chat_member(message.chat_id, message.from_user_id)
        logging.info(f"user {message.from_user_full_name} banned in {message.chat_title}")
    except aiogram.exceptions.TelegramBadRequest:
        logging.warning(
            f"user {message.from_user_id} could be banned, but bot has no access to ban in group {message.chat_id}"
        )
