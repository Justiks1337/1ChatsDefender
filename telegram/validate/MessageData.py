from dataclasses import dataclass
from typing import List

from telegram.validate.sentinels import UNSET, UnsetType


@dataclass(kw_only=True)
class MessageData:
    """Содержит компоненты Telegram-сообщения, необходимые для проверок.

    Хранит текст, идентификаторы сообщения, отправителя и чата, а также
    другие сведения, используемые обработчиками.

    Добавляйте поля, когда они нужны цепочке проверок. Все новые поля
    должны оставаться необязательными. UNSET обозначает незаданное поле,
    а None — явно указанное отсутствие значения.
    """

    message_id: int | None | UnsetType = UNSET

    text: str | None | UnsetType = UNSET
    caption: str | None | UnsetType = UNSET

    from_user_id: int | None | UnsetType = UNSET
    from_user_full_name: str | None | UnsetType = UNSET
    from_user_is_bot: bool | None | UnsetType = UNSET

    chat_id: int | None | UnsetType = UNSET
    chat_title: str | None | UnsetType = UNSET

    story: bool | None | UnsetType = UNSET  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
    reply_markup: bool | None | UnsetType = UNSET  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
    photo: List | None | UnsetType = UNSET  # TODO: В данный момент поле зависит от aiogram, оставил так для обратной совместимости
    new_chat_members: bool | None | UnsetType = UNSET  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
    external_reply: bool | None | UnsetType = UNSET  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
