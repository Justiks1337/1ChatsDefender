from telegram.middleware.AbstractHandler import AbstractHandler
from telegram.validate.Context import Context
from telegram.Counter import Counter


class CounterMiddleware(AbstractHandler):
    """
    Этот middleware считает статистику по боту
    """

    async def execute(self, context: Context) -> None:
        """
        Главный метод в middleware

        :param context: Адаптер сообщения
        :return: None
        """

        counter = Counter()

        # Если сообщение подлежит удалению
        if context.punishment is not None:
            counter.messages_deleted += 1
