from telegram.validate.Context import Context
from telegram.validate.handlers.AbstractHandler import AbstractHandler


class EmptyHandler(AbstractHandler):
    """
    Handler с которого должны начинаться все Chains
    """

    async def handle(self, message: Context):
        if self._next_handler:
            return await self._next_handler.handle(message)

        return message

    def is_available(self) -> bool:
        return True
