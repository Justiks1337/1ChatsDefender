import logging

from telegram.Context import Context
from telegram.punishments import warning
from utils.patterns.chain_of_responsibility import AbstractHandler


class UpperCaseHandler(AbstractHandler):
    """
    Проверка сообщения на caps
    """

    # Процент капса в сообщении, после которого сообщение удаляется
    CAPS_PERCENTAGE = 0.7

    # Дабы не допустить ситуацию, в которой удаляется сообщение состоящее из одного символа, ограничим минимальное количество символов в сообщении
    MINIMUM_SYMBOLS = 10

    async def handle(self, message: Context):
        message_text = message.message.text
        message_caption = message.message.caption
        if not isinstance(message_text, str) and not isinstance(message_caption, str):
            logging.debug("UpperCaseHandler пропущен: text и caption не установлены")
            return await super().handle(message)

        text = False
        caption = False
        if isinstance(message_text, str):
            if len(message_text) > self.MINIMUM_SYMBOLS:
                text = self.__check(message_text)

        if isinstance(message_caption, str):
            if len(message_caption) > self.MINIMUM_SYMBOLS:
                caption = self.__check(message_caption)

        if caption or text:
            message.is_trusted = False
            message.execute = warning(message.message)
            logging.info("Upper Case Handler is worked now")
            return message

        return await super().handle(message)

    def __check(self, text: str) -> bool:
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
