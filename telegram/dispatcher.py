"""In this file initialize
the dispatcher instance, to avoid circular imports in future
"""

import os

from aiogram import Dispatcher, Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv(".env.telegram")
load_dotenv(".env")


# Сессия с socks5 proxy для бота
session = AiohttpSession(proxy=os.getenv("PROXY_URL"))

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(os.getenv("BOT_TOKEN"), session=session)
