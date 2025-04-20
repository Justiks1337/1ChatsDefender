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

def is_running_under_unittest():
    return ('unittest' in sys.modules or any('unittest' in arg for arg in sys.argv) or sys.argv[0].endswith('pytest') or 'pytest' in sys.modules)


dp = Dispatcher(storage=MemoryStorage())
bot = Bot(os.getenv("BOT_TOKEN"))
