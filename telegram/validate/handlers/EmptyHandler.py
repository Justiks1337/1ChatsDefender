from telegram.validate.Context import Context
from telegram.validate.handlers.AbstractHandler import AbstractHandler


class EmptyHandler(AbstractHandler):
    """Служит начальным обработчиком для всех цепочек проверок.

    Не выполняет собственных проверок и передаёт контекст следующему звену.
    Если цепочка пуста, возвращает исходный контекст.
    """

    async def handle(self, message: Context):
        if self._next_handler:
            return await self._next_handler.handle(message)

        return message

    def is_available(self) -> bool:
        return True
