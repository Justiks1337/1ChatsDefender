from collections.abc import Awaitable, Callable

from telegram.validate.Context import Context
from telegram.validate.MessageData import MessageData
from telegram.validate.PunishmentCommand import PunishmentType
from telegram.middleware.MiddlewareInterface import MiddlewareInterface
from telegram.punishments import ban, delete, warning


PunishmentHandler = Callable[[MessageData], Awaitable[None]]


class PunishmentMiddleware(MiddlewareInterface):
    _handlers: dict[PunishmentType, PunishmentHandler] = {
        PunishmentType.DELETE: delete,
        PunishmentType.WARNING: warning,
        PunishmentType.BAN: ban,
    }

    @classmethod
    async def execute(cls, context: Context) -> Context:
        command = context.punishment
        if command is None:
            return context

        punishment_handler = cls._handlers[command.type]
        await punishment_handler(context.message)
        return context
