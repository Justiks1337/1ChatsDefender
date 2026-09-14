import time
import logging
from typing import List, Dict

from telegram.validate.MessageData import MessageData

from telegram.dispatcher import bot
from utils.patterns.singleton import Singleton


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

    async def is_admin(self, message: MessageData) -> bool:
        """
        check message author is admin by aiogram.types.Message object
        replace ChatAdminFabric.get by this
        :param message: aiogram Message object
        :return True if message author is admin else False
        """

        if isinstance(message.from_user_id, int):
            if isinstance(message.chat_id, int):
                admins = await self.get(message.chat_id)
                if message.from_user_id in admins:
                    return True
            else:
                logging.warning("admin_management, MessageData not contains message.chat_id")
        else:
            logging.warning("admin_management, MessageData not contains message.from_user_id")

        # bot.get_chat_administrators (using in self.__get_administrators_from_server) isn't return anonymous chat administrators
        # in this case anonymous administrator isn't trusted
        # check user is admin by User.is_bot = True

        if isinstance(message.from_user_is_bot, int):
            if message.from_user_is_bot:
                return True

        # member is not admin
        return False

    async def get(self, chat_id: int) -> AdministratorsCache:
        """get a current chat administrators, from cache and """

        # Attempt get administrators from cache
        administrators_from_cache = self.__get_administrators_from_cache(chat_id)

        if administrators_from_cache:
            return administrators_from_cache

        # Attempt get administrators from server
        return await self.__get_administrators_from_server(chat_id)

    def __get_administrators_from_cache(self, chat_id: int) -> AdministratorsCache | None:
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
