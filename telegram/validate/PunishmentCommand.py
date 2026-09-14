from dataclasses import dataclass
from enum import Enum, auto


class PunishmentType(Enum):
    """Перечисляет наказания, применяемые при обработке сообщения.

    Поддерживает удаление сообщения, предупреждение и бан пользователя.
    """
    DELETE = auto()
    WARNING = auto()
    BAN = auto()


@dataclass(frozen=True, slots=True)
class PunishmentCommand:
    """Хранит информацию о наказании, назначенном за сообщение.

    Содержит тип наказания, необязательную причину и источник решения.
    После создания команда неизменяема и передаётся на исполнение middleware.
    """
    type: PunishmentType
    reason: str | None = None
    source: str | None = None
