import logging

from telegram.validate.Context import Context
from telegram.validate.PunishmentCommand import PunishmentCommand, PunishmentType
from telegram.validate.handlers.AbstractHandler import AbstractHandler


class UpperCaseHandler(AbstractHandler):
    """
    Проверка сообщения на caps
    """

    # Процент капса в сообщении, после которого сообщение удаляется
    CAPS_PERCENTAGE = 0.7

    # Дабы не допустить ситуацию, в которой удаляется сообщение состоящее из одного символа, ограничим минимальное количество символов в сообщении
    MINIMUM_SYMBOLS = 10

    def _check_message(self, text: object, caption: object) -> bool:
        text_result = (
            isinstance(text, str)
            and len(text) > self.MINIMUM_SYMBOLS
            and self._check_text(text)
        )
        caption_result = (
            isinstance(caption, str)
            and len(caption) > self.MINIMUM_SYMBOLS
            and self._check_text(caption)
        )
        return text_result or caption_result

    async def handle(self, message: Context):
        message_text = message.message.text
        message_caption = message.message.caption
        if not isinstance(message_text, str) and not isinstance(message_caption, str):
            logging.debug("UpperCaseHandler пропущен: text и caption не установлены")
            return await super().handle(message)

        if self._check_message(message_text, message_caption):
            message.is_trusted = False
            message.punishment = PunishmentCommand(
                PunishmentType.WARNING,
                reason="Превышен допустимый процент заглавных букв",
                source=type(self).__name__,
            )
            logging.info("Upper Case Handler is worked now")
            return message

        return await super().handle(message)

    def _check_text(self, text: str) -> bool:
        """
        Проверьте сообщение на капс и верните bool
        :return: True, если сообщение превышает лимиты, иначе False
        """

        len_of_message = len(text)

        # Далее я проверяю сообщение на капс
        # Я делю сообщение на три части, дабы не совершать лишних проверок
        # В первой части я просто считаю uppercase символы
        # Во второй я проверяю не является ли 1 - CAPS_PERCENTAGE символов в сообщении lowercased
        # В третьей я совмещаю предыдущие проверки + проверку на CAPS_PERCENTAGE uppercase символов в сообщении

        first_cut = round(len_of_message * (1 - self.CAPS_PERCENTAGE))
        second_cut = round(len_of_message * self.CAPS_PERCENTAGE)

        first_part = text[:first_cut]
        second_part = text[first_cut:second_cut]
        third_part = text[second_cut:]

        uppercased_symbols = 0
        lowercased_symbols = 0

        for symbol in first_part:
            if symbol.isupper():
                uppercased_symbols += 1
            else:
                lowercased_symbols += 1

        for symbol in second_part:
            if symbol.isupper():
                uppercased_symbols += 1
            else:
                lowercased_symbols += 1

            # Обратная проверка снизу, на 1-self.CAPS_PERCENTAGE lowercased symbols
            if lowercased_symbols / len_of_message >= 1 - self.CAPS_PERCENTAGE:
                return False

        for symbol in third_part:
            if symbol.isupper():
                uppercased_symbols += 1
            else:
                lowercased_symbols += 1

            # Обратная проверка снизу, на 1-self.CAPS_PERCENTAGE lowercased symbols
            if lowercased_symbols / len_of_message >= 1 - self.CAPS_PERCENTAGE:
                return False
            if uppercased_symbols / len_of_message >= self.CAPS_PERCENTAGE:
                return True

        # На всякий случай, если произойдет исход когда не одно из условий не сработало (по идее не возможно)
        return False

    def is_available(self) -> bool:
        return True
