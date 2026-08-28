from telegram.Context import Context
from utils.patterns.chain_of_responsibility import AbstractHandler


class EmptyHandler(AbstractHandler):
    """
    Handler с которого должны начинаться все Chains
    """

    async def handle(self, message: Context):
        if self._next_handler:
            return await self._next_handler.handle(message)

        return message
