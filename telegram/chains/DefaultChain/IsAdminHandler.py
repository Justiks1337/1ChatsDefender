import logging
from typing import List, Dict
import time

from utils import AbstractHandler, Singleton

from telegram.Message import Message
from telegram.dispatcher import bot
from telegram.punishments import delete


class IsAdminHandler(AbstractHandler):

    async def handle(self, message: Message) -> Message:
        if message.message.from_user.id in await ChatAdminsFabric().get(message.message.chat.id):
            logging.debug("IsAdminHandler is worked now")
            message.next_handler = False
            return message
        return await super().handle(message)


class AdministratorsCache:
    
    """This class instances implements administrators cache"""

    INSTANCE_LIFE_TIME = 86400

    def __init__(self, admins):
        self._admins: List[int] = admins
        self.__created_at = time.time()

    def is_valid(self):
        return time.time() - 86400 < self.__created_at

    def __contains__(self, item: int):
        return item in self._admins


class ChatAdminsFabric(Singleton):

    """
    ChatAdminsFabric

    First, the algorithm tries to get the administrators' IDs from this dict;
    if it did not work, then a request is made to the servers

    cache stored in instance dict - cached_chat_administrators Pairs - chat_id: array of Administrator instances
                                                    """

    def init(self):
        self.cached_chat_administrators: Dict[int, AdministratorsCache] = {}

    async def get(self, chat_id: int) -> AdministratorsCache:
        """get a current chat administrators, from cache and """

        # Attempt get administrators from cache
        administrators_from_cache = self.__get_administrators_from_cache(chat_id)

        if administrators_from_cache:
            return administrators_from_cache

        # Attempt get administrators from server
        return await self.__get_administrators_from_server(chat_id)

    def __get_administrators_from_cache(self, chat_id: int) -> AdministratorsCache:
        administrators = self.cached_chat_administrators.get(chat_id)

        # administrators may be is None, that's why I use isinstance. If it is not None, check validity
        if isinstance(administrators, AdministratorsCache) and administrators.is_valid():
            return administrators

    async def __get_administrators_from_server(self, chat_id: int) -> AdministratorsCache:

        aiogram_administrators = await bot.get_chat_administrators(chat_id)
        administrators = []

        for admin in aiogram_administrators:
            administrators.append(admin.user.id)
        administrators_instance = AdministratorsCache(administrators)

        # Update cache
        self.__to_cache(chat_id, administrators_instance)

        return administrators_instance

    def __to_cache(self, chat_id: int, administrators: AdministratorsCache):
        if self.cached_chat_administrators.get(chat_id):
            del self.cached_chat_administrators[chat_id]

        self.cached_chat_administrators[chat_id] = administrators
