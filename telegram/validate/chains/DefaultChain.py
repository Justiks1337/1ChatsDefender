import logging

from telegram.validate.handlers import AbstractHandler
from telegram.validate.Context import Context
from telegram.validate.handlers.IsJoinMessageHandler import IsJoinMessageHandler
from telegram.validate.handlers import IsAdminHandler
from telegram.validate.handlers import RegexHandler
from telegram.validate.handlers import IsGroupHandler
from telegram.validate.handlers import EmptyHandler


class DefaultChain(AbstractHandler):
    """Объединяет базовые проверки входящих сообщений.

    Проверяет личный чат, уведомления о вступлении, права администратора
    и запрещённые выражения. Продолжает обработку следующей цепочкой,
    если наказание не назначено и дальнейшие проверки разрешены.
    """

    def __init__(self):
        self.first_handler = EmptyHandler()
        handlers = [
            IsGroupHandler(),
            IsJoinMessageHandler(),
            IsAdminHandler(),
            RegexHandler(),
        ]

        current_handler = self.first_handler
        for handler in handlers:
            if handler.is_available():
                current_handler = current_handler.set_next(handler)

    async def handle(self, message: Context):
        result: Context = await self.first_handler.handle(message)

        if result.punishment is not None or not result.next_handler:
            logging.info("Default chain handle a violation.")
            return result

        return await super().handle(message)

    def is_available(self) -> bool:
        return True
