from telegram.middleware.MiddlewareInterface import MiddlewareInterface
from telegram.Message import Message
from telegram.Counter import Counter


class CounterMiddleware(MiddlewareInterface):
    """
    Этот middleware считает статистику по боту
    """

    @classmethod
    async def execute(cls, message: Message) -> Message:
        """
        Главный метод в middleware

        :param message: Адаптер сообщения
        :return: Измененный адаптер сообщения из аргументов
        """

        counter = Counter()

        # Если сообщение подлежит удалению
        if not message.is_trusted:
            counter.messages_deleted += 1

        # Добавляем к счетчику удаленных сообщений
        counter.messages_handled += 1

        return message

