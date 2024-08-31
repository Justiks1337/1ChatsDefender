from aiogram.types import Message

from telegram.dispatcher import dp
from telegram.router import Router


@dp.message()
async def main_handler(message: Message):
    await Router().to_route(message)
