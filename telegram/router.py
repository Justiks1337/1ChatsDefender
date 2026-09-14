from aiogram.types import Message as AiogramMessage

from telegram.AiogramMessageMapper import AiogramMessageMapper
from telegram.Counter import Counter
from telegram.middleware import middlewares
from telegram.validate.Context import Context
from telegram.validate.chains.DefaultChain import DefaultChain
from telegram.validate.chains.SuperGroupChain import SuperGroupChain
from utils import Singleton


class Router(Singleton):

    def init(self):
        self.default_chain = DefaultChain()
        self.super_group_chain = SuperGroupChain()

        self.default_chain.set_next(self.super_group_chain)

        self.middleware_chain = None
        current_middleware = None
        for handler in middlewares:
            if current_middleware is None:
                self.middleware_chain = handler
            else:
                current_middleware.set_next(handler)

            current_middleware = handler

    async def to_route(self, message: AiogramMessage):
        """
        Start message validate

        :param message: telegram.Context.Context
        :return: None
        """

        context = Context(AiogramMessageMapper.map(message))
        context = await self.__validate_message(context)
        await self.__execute_middleware(context)

        counter = Counter()
        counter.messages_handled += 1

    async def __validate_message(self, message: Context):
        """
        Start a chain of checks for message

        :param message: telegram.Context.Context
        :return: validate message
        """

        return await self.default_chain.handle(message)

    async def __execute_middleware(self, message: Context) -> Context:
        """
        Выполнить цепочку middleware для сообщения.

        :param message: Контекст сообщения.
        :return: Контекст после выполнения цепочки.
        """

        if self.middleware_chain is None:
            return message

        return await self.middleware_chain.handle(message)
