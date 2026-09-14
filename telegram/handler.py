import json
import logging
import time

from aiogram import Router as AiogramRouter
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.serialization import deserialize_telegram_object_to_python

from telegram.Counter import Counter
from telegram.admin_management import ChatAdminsFabric
from telegram.punishments import ban
from telegram.router import Router
from utils.database.connection import DatabaseConnection
from telegram.AiogramMessageMapper import AiogramMessageMapper
from telegram.validate.MessageData import MessageData

router = AiogramRouter()


@router.message(Command("ban"))
async def ban_command_handler(message: Message):
    """delete reply_to_message and write it to database"""

    # check user is admin

    message_data: MessageData = AiogramMessageMapper.map(message)
    # TODO: Перед /ban проверять актуальные права администратора: кеш на сутки
    # позволяет выполнять команду после снятия прав.
    if not await ChatAdminsFabric().is_admin(message_data):
        return

    if not message.reply_to_message:
        return

    # ban user
    ban_message = message.reply_to_message
    await ban(AiogramMessageMapper.map(ban_message))

    # clear chat
    await message.delete()

    # write to database
    await DatabaseConnection().save_banned_message(
        ban_message.text if ban_message.text is not None else ban_message.caption,
        json.dumps(deserialize_telegram_object_to_python(ban_message), ensure_ascii=False, indent=4, default=str),
    )


@router.message(Command("ping"))
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


@router.edited_message()
@router.message()
async def main_handler(message: Message) -> None:
    """
    Хендлер, который слушает все входящие в него сообщения
    :param message: aiogram.Message объект
    :return: None
    """
    logging.debug(f"handle a message - {message.text}")
    await Router().to_route(message)
