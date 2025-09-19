import logging
import datetime
import time

from aiogram.filters.command import Command
from aiogram.types import Message

from telegram.admin_management import ChatAdminsFabric
from telegram.punishments import ban
from telegram.dispatcher import dp
from telegram.router import Router
from telegram.Counter import Counter
from utils.database.connection import DatabaseConnection


@dp.message(Command("ban"))
async def ban_command_handler(message: Message):
    """delete reply_to_message and write it to database"""

    # check user is admin
    if not await ChatAdminsFabric().is_admin(message):
        return

    if not message.reply_to_message:
        return

    # ban user
    ban_message = message.reply_to_message
    await ban(ban_message)

    # clear chat
    await message.delete()

    # write to database
    connect = DatabaseConnection().connect

    await connect.execute("INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        ban_message.text,
        ban_message.from_user.id,
        ban_message.date,
        ban_message.from_user.full_name,
        ban_message.from_user.username,
        ban_message.from_user.language_code,
        ban_message.from_user.is_premium,
        int(bool(ban_message.forward_origin)),
        0  # bot can't get access to message.reply_to_message.reply_to_message. Always is false
    )
    )

    await connect.commit()


@dp.message(Command("ping"))
async def ping_command_handler(message: Message):
    """
    /ping command handler (cosmetic)
    :param message: aiogram Message
    :return: None
    """
    counter = Counter()

    total_seconds = int(time.time() - counter.start_time)

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []
    if days > 0:
        parts.append(f"{days} д")
    if hours > 0:
        parts.append(f"{hours} ч")
    if minutes > 0:
        parts.append(f"{minutes} мин")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} сек")

    uptime = " ".join(parts)

    message_text = ("🟢 Статус бота - работает \n\n"
                    f"Uptime: {uptime}\n"
                    f"Удалено сообщений: {counter.messages_deleted}\n"
                    f"Просмотрено сообщений {counter.messages_handled}\n\n"
                    f"Мяу")

    await message.answer(message_text)


@dp.message()
async def main_handler(message: Message):
    logging.debug(f"handle a message - {message.text}")
    await Router().to_route(message)
