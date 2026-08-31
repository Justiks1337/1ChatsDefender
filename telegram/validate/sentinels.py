class UnsetType:
    """Тип значения для незаданных атрибутов."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "UNSET"


UNSET = UnsetType()
