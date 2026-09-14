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
        if not context.is_trusted:
            counter.messages_deleted += 1
