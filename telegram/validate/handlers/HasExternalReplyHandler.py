import logging

from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType
from telegram.validate.handlers import AbstractHandler


class HasExternalReplyHandler(AbstractHandler):
    """Запрашивает удаление сообщения с внешним ответом и бан отправителя.

    Мошенники используют внешние ответы для размещения неявных ссылок
    на нужный им контент. Например, нейтральное сообщение может содержать
    ответ на рекламную публикацию из другого чата.

    Исходная предпосылка проверки: Telegram Bot API сообщает о наличии
    внешнего ответа, но не позволяет прочитать его содержимое; иной способ
    модерации таких ответов в рамках Telegram TOS при разработке не был
    предусмотрен. Здесь проверяется только признак external_reply.

    Правило исходит из того, что обычные участники редко используют внешние
    ответы, поэтому любое сообщение с external_reply=True подозрительно.
    Размещайте обработчик после IsTrustedMemberHandler, чтобы снизить риск
    блокировки добросовестного участника.

    При срабатывании назначает бан, исполнение которого включает удаление
    сообщения. Содержимое внешнего ответа не анализируется.
    """

    def _check_message(self, external_reply: object) -> bool:
        return isinstance(external_reply, bool) and external_reply

    async def handle(self, message: Context):
        if not isinstance(message.message.external_reply, bool):
            logging.debug("HasExternalReplyHandler пропущен: external_reply не установлен")
            return await super().handle(message)

        # Проверяем, есть ли external_reply в сообщении
        if self._check_message(message.message.external_reply):
            # Если ест1ь external_reply, то автор сообщения должен быть забанен
            message.punishment = PunishmentCommand(
                PunishmentType.BAN,
                reason="Обнаружен внешний ответ",
                source=type(self).__name__,
            )
            logging.info("HasExternalReplyHandler worked - user banned for external reply")
            return message

        # Если external_reply отсутствует, продолжаем цепочку
        return await super().handle(message)

    def is_available(self) -> bool:
        return True
