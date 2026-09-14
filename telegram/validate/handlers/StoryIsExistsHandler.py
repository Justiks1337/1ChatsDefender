import logging

from telegram.validate.Context import Context
from telegram.validate.handlers import AbstractHandler
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType


class StoryIsExistsHandler(AbstractHandler):
    """Запрашивает удаление сообщения с пересланной историей и бан отправителя.

    Мошенники пересылают Telegram-истории, чтобы показать нужный им контент.
    Например, реклама может находиться внутри истории, тогда как текст
    сообщения не содержит запрещённых выражений.

    Исходная предпосылка проверки: Telegram Bot API сообщает об источнике
    и наличии истории, но не позволяет получить её содержимое; иной способ
    модерации историй в рамках Telegram TOS при разработке не был
    предусмотрен. Здесь проверяется только признак story.

    Правило исходит из того, что обычные участники редко пересылают истории,
    поэтому любое сообщение с историей считается подозрительным.
    В MessageData наличие истории представлено значением story=True.
    Размещайте обработчик после IsTrustedMemberHandler, чтобы снизить риск
    блокировки добросовестного участника.

    При срабатывании назначает бан, исполнение которого включает удаление
    сообщения. Содержимое истории не анализируется.
    """

    def _check_message(self, story: object) -> bool:
        return isinstance(story, bool) and story

    async def handle(self, message: Context):
        if not isinstance(message.message.story, bool):
            logging.debug("StoryIsExistsHandler пропущен: story не установлен")
            return await super().handle(message)

        if self._check_message(message.message.story):
            message.punishment = PunishmentCommand(
                PunishmentType.BAN,
                reason="Обнаружена история",
                source=type(self).__name__,
            )
            logging.debug("HistoryIsExistsHandler is working now")
            return message

        return await super().handle(message)

    def is_available(self) -> bool:
        return True
