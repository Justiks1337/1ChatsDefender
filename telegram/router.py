import asyncio

from utils import Singleton

from telegram.Message import Message
from telegram.middleware import middlewares
from telegram.chains.DefaultChain.DefaultChain import DefaultChain
from telegram.chains.SuperGroupChain.SuperGroupChain import SuperGroupChain


class Router(Singleton):

    async def to_route(self, message: Message):
        """
        Start message validate

        :param message: telegram.Message.Message
        :return: None
        """

        await self.execute_punishment(await self.execute_middleware(await self.validate_message(message)))

    async def validate_message(self, message: Message):
        """
        Start a chain of checks for message

        :param message: telegram.Message.Message
        :return: validate message
        """
        default_chain = DefaultChain()
        super_group_chain = SuperGroupChain()

        default_chain.set_next(super_group_chain)

        message = await default_chain.handle(message)

        return message

    async def execute_middleware(self, message):
        """
        Execute all middlewares for this message

        :param message:  telegram.Message.Message
        :return: edited message by middlewares
        """

        index = 0  # cursor

        for middleware in middlewares:
            message = middleware.execute(message)

        return message

    async def execute_punishment(self, message: Message):
        """
        End message validate, Verdict.

        :param message: telegram.Message.Message
        :return: None
        """

        punishment = message.execute

        if asyncio.iscoroutine(punishment):
            await punishment
