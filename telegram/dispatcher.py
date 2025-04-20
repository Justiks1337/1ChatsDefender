"""In this file initialize
the dispatcher instance, to avoid circular imports in future
"""

import os
import sys

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv(".env.telegram")


# Костыль, проверяет запущен ли скрипт в unittest контексте
# TODO: Внимание, тесты должны быть изолированы, и это нужно исправить!
if not getattr(sys, "_called_from_test", False):
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(os.getenv("BOT_TOKEN"))
else:
    dp = None
    bot = None
