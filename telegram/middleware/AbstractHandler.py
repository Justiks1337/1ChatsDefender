from __future__ import annotations

import logging

from typing import Optional, final
from abc import ABC, abstractmethod

from telegram.validate.Context import Context


class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    async def handle(self, context: Context) -> Context:
        pass

    @abstractmethod
    async def execute(self, context: Context) -> None:
        pass


# TODO: Решить проблему повторяющегося кода цепочки обязанностей
# в middleware и telegram/validate/handlers/AbstractHandler.py.
class AbstractHandler(Handler):
    """Выполняет middleware и передаёт результат следующему обработчику."""

    async def execute(self, context: Context) -> None:
        raise NotImplementedError("execute(context: Context) not implemented")

    def __init__(self):
        self._next_handler: Optional[AbstractHandler] = None

    def set_next(self, handler: AbstractHandler) -> AbstractHandler:
        self._next_handler = handler
        return handler

    @final
    async def handle(self, context: Context) -> Context:
        try:
            await self.execute(context)
        except Exception:
            logging.exception(
                "Ошибка выполнения middleware %s",
                type(self).__name__,
            )

        if self._next_handler is not None:
            return await self._next_handler.handle(context)

        return context
