"""In this file initialize
the dispatcher instance, to avoid circular imports in future
"""

import os

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from telegram.router import Router

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(os.getenv("BOT_TOKEN"))
Router()  # router - singleton. This line execute initial Router method
