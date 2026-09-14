from collections.abc import Awaitable, Callable

from telegram.validate.Context import Context
from telegram.validate.MessageData import MessageData
from telegram.validate.PunishmentCommand import PunishmentType
from telegram.middleware.AbstractHandler import AbstractHandler
from telegram.punishments import ban, delete, warning


PunishmentHandler = Callable[[MessageData], Awaitable[None]]


class PunishmentMiddleware(AbstractHandler):
    _handlers: dict[PunishmentType, PunishmentHandler] = {
        PunishmentType.DELETE: delete,
        PunishmentType.WARNING: warning,
        PunishmentType.BAN: ban,
    }

    async def execute(self, context: Context) -> None:
        command = context.punishment
        if command is None:
            return

        punishment_handler = self._handlers[command.type]
        await punishment_handler(context.message)
