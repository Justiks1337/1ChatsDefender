from abc import ABC, abstractmethod


class MiddlewareInterface(ABC):

    @classmethod
    @abstractmethod
    async def execute(cls, message):
        pass
