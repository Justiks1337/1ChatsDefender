import logging

from aiogram.types import Message

from telegram.dispatcher import dp
from telegram.router import Router


@dp.message()
async def main_handler(message: Message):
    logging.debug(f"handle a message - {message.text}")
    await Router().to_route(message)
