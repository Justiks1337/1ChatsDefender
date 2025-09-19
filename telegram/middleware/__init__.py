from telegram.middleware.MiddlewareInterface import MiddlewareInterface
from telegram.middleware.MessageToDatabaseMiddleware import MessageToDatabaseMiddleware
from telegram.middleware.SendMessageMiddleware import SendMessageMiddleware
from telegram.middleware.CounterMiddleware import CounterMiddleware

"""
middlewares - array with middlewares.
Each middleware from this array is called.
The call takes place alternately
"""

middlewares = [
    SendMessageMiddleware,
    MessageToDatabaseMiddleware,
    CounterMiddleware
]
