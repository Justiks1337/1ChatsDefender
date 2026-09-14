class UnsetType:
    """Представляет значение незаданного атрибута.

    Экземпляр UNSET позволяет отличать незаданное поле от явного None.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        return "UNSET"


UNSET = UnsetType()
