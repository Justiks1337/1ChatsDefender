from telegram.middleware.AbstractHandler import AbstractHandler
from telegram.validate.Context import Context
from telegram.Counter import Counter


class CounterMiddleware(AbstractHandler):
    """Собирает статистику модерации для общего счётчика бота.

    Для сообщений с назначенным наказанием увеличивает messages_deleted.
    Счётчик отражает назначенные наказания, а не подтверждение удаления.
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
