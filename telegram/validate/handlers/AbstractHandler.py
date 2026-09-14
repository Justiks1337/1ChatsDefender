from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional


class Handler(ABC):
    """Определяет интерфейс построения цепочки и выполнения запросов.

    Метод set_next связывает обработчики, а handle запускает обработку.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    async def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """Реализует стандартное поведение звена цепочки проверок.

    Базовый класс связывает обработчики и передаёт запрос следующему звену.
    Подклассы дополняют handle своей проверкой и определяют доступность
    через is_available.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    async def handle(self, request: Any) -> Any:  # In original pattern is sync, but I use async in my project
        if self._next_handler:
            return await self._next_handler.handle(request)

        return request

    @abstractmethod
    def is_available(self) -> bool:
        """Вернуть True, если доступны все зависимости, необходимые обработчику."""
        raise NotImplementedError
