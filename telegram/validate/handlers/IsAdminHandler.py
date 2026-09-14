import logging

from telegram.validate.handlers import AbstractHandler

from telegram.validate.Context import Context


class IsAdminHandler(AbstractHandler):
    """Останавливает цепочку проверок для сообщений администраторов чата.

    Сообщения администраторов считаются доверенными и освобождаются
    от дальнейших проверок. Например, объявление администратора
    не должно блокироваться последующими фильтрами запрещённых слов.

    Проверяет права через ChatAdminsFabric и устанавливает next_handler=False.
    Отдельный признак доверия в контексте не устанавливает.
    """

    def __init__(self):
        self.__available = True

        try:
            from telegram.admin_management import ChatAdminsFabric
            self.__chat_admins_fabric = ChatAdminsFabric()

        except ImportError:
            self.__available = False
            logging.error(
                "Не удалось загрузить IsAdminHandler из-за недостающей зависимости"
            )

    async def handle(self, message: Context) -> Context:
        if not isinstance(message.message.chat_id, int) or not isinstance(message.message.from_user_id, int):
            logging.debug("IsAdminHandler пропущен: chat_id или from_user_id не установлен")
            return await super().handle(message)

        if await self.__chat_admins_fabric.is_admin(message.message):
            logging.debug("IsAdminHandler is worked now")
            message.next_handler = False
            return message
        return await super().handle(message)

    def is_available(self) -> bool:
        return self.__available
