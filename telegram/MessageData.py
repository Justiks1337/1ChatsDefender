from dataclasses import dataclass
from typing import List

from telegram.sentinels import UNSET, UnsetType


@dataclass(kw_only=True)
class MessageData:
    """
    Объект содержит компоненты из которых состоит сообщение Telegram, такие как текст сообщения, айди сообщения и прочее
    Добавьте новое поле, при его необходимости в цепочке проверок
    Все создаваемые поля должны быть опциональными.

    """

    text: str | None | UnsetType = UNSET
    caption: str | None | UnsetType = UNSET

    from_user_id: int | None | UnsetType = UNSET
    from_user_full_name: str | None | UnsetType = UNSET
    from_user_is_bot: bool | None | UnsetType = UNSET
    from_user_full_name: bool | None | UnsetType = Unset

    chat_id: int | None | UnsetType = UNSET
    chat_title: str | None | UnsetType = UNSET

    story: bool | None | UnsetType = UNSET  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
    reply_markup: bool | None | UnsetType = UNSET  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
    photo: List | None | UnsetType = UNSET  # TODO: В данный момент поле зависит от aiogram, оставил так для обратной совместимости
    new_chat_members: bool | None | UnsetType = UNSET  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
    external_reply: bool | None | UnsetType = UNSET  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
