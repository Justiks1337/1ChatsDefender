from dataclasses import dataclass
from enum import Enum, auto


class PunishmentType(Enum):
    DELETE = auto()
    WARNING = auto()
    BAN = auto()


@dataclass(frozen=True, slots=True)
class PunishmentCommand:
    type: PunishmentType
    reason: str | None = None
    source: str | None = None
