import logging

from telegram.validate.handlers import AbstractHandler
from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType


class ManySpacesHandler(AbstractHandler):
    """Запрашивает удаление сообщения с избыточной долей пробелов.

    Мошенники разделяют слова на буквы пробелами, чтобы обойти поиск
    запрещённых выражений: например, пишут «з а р а б о т о к» вместо
    цельного слова. Проверка выявляет такой способ маскировки текста.

    Сообщение считается подозрительным, если доля обычных пробелов
    в тексте или подписи превышает допустимый порог — 35%.
    Поля проверяются отдельно; пустые значения пропускаются.

    Назначает предупреждение, исполнение которого включает удаление сообщения.
    """
    def _check_message(self, text: object, caption: object) -> bool:
        return not (self._validate_text(text) and self._validate_text(caption))

    async def handle(self, message: Context):

        text = message.message.text
        caption = message.message.caption
        if not isinstance(text, str) and not isinstance(caption, str):
            logging.debug("ManySpacesHandler пропущен: text и caption не установлены")
            return await super().handle(message)

        if self._check_message(text, caption):
            message.punishment = PunishmentCommand(
                PunishmentType.WARNING,
                reason="Слишком много пробелов",
                source=type(self).__name__,
            )
            logging.info("ManySpacesHandler is worked now")
            return message

        return await super().handle(message)

    def _validate_text(self, text: object) -> bool:
        if not isinstance(text, str) or not text:
            return True

        return not (text.count(" ") / len(text) * 100 > 35)

    def is_available(self) -> bool:
        return True
