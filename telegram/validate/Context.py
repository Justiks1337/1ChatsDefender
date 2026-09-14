from telegram.validate.MessageData import MessageData
from telegram.validate.PunishmentCommand import PunishmentCommand


class Context:

    """Передаёт данные и состояние сообщения по цепочке проверок.

    Атрибуты:
        message: Датакласс MessageData с информацией, необходимой проверкам.
        punishment: Команда наказания, исполняемая на этапе middleware.
        next_handler: Признак, разрешающий продолжение проверок.
    """

    def __init__(self, message: MessageData):
        self.__message: MessageData = message
        self._punishment: PunishmentCommand | None = None
        self._next_handler = True

    @property
    def message(self):
        return self.__message

    @property
    def punishment(self) -> PunishmentCommand | None:
        return self._punishment

    @punishment.setter
    def punishment(self, value: PunishmentCommand | None):
        self._punishment = value

    @property
    def next_handler(self):
        return self._next_handler

    @next_handler.setter
    def next_handler(self, value):
        self._next_handler = value
