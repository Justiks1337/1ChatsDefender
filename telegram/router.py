from aiogram.types import Message as AiogramMessage

from telegram.AiogramMessageMapper import AiogramMessageMapper
from telegram.Counter import Counter
from utils import Singleton
from telegram.validate.Context import Context
from telegram.middleware import middlewares
from telegram.middleware.PunishmentMiddleware import PunishmentMiddleware
from telegram.validate.chains.DefaultChain import DefaultChain
from telegram.validate.chains.SuperGroupChain import SuperGroupChain


class Router(Singleton):

    def init(self):
        self.default_chain = DefaultChain()
        self.super_group_chain = SuperGroupChain()

        self.default_chain.set_next(self.super_group_chain)

    async def to_route(self, message: AiogramMessage):
        """
        Start message validate

        :param message: telegram.Context.Context
        :return: None
        """

        context = Context(AiogramMessageMapper.map(message))
        context = await self.__validate_message(context)
        context = await self.__execute_middleware(context)
        await PunishmentMiddleware.execute(context)

        counter = Counter()
        counter.messages_handled += 1

    async def __validate_message(self, message: Context):
        """
        Start a chain of checks for message

        :param message: telegram.Context.Context
        :return: validate message
        """

        return await self.default_chain.handle(message)

    async def __execute_middleware(self, message):
        """
        Execute all middlewares for this message

        :param message:  telegram.Context.Context
        :return: edited message by middlewares
        """

        if not message.execute_middleware:
            return message

        for middleware in middlewares:
            message = await middleware.execute(message)

        return message
