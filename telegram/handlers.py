from aiogram.types import Message

from telegram.dispatcher import dp


@dp.message()
async def main_handler(message: Message):
    pass
