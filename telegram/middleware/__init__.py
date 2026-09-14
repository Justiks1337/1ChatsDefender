from telegram.middleware.AbstractHandler import Handler
from telegram.middleware.CounterMiddleware import CounterMiddleware
from telegram.middleware.MessageToDatabaseMiddleware import MessageToDatabaseMiddleware
from telegram.middleware.PunishmentMiddleware import PunishmentMiddleware
from telegram.middleware.SendMessageMiddleware import SendMessageMiddleware

"""Экземпляры middleware в порядке выполнения."""

middlewares: list[Handler] = [
    PunishmentMiddleware(),
    SendMessageMiddleware(),
    MessageToDatabaseMiddleware(),
    CounterMiddleware(),
]
