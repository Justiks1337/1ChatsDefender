from dataclasses import dataclass
from typing import List


@dataclass
class MessageData:
    """
    Объект содержит компоненты из которых состоит сообщение Telegram, такие как текст сообщения, айди сообщения и прочее
    Добавьте новое поле, при его необходимости в цепочке проверок
    Все создаваемые поля должны быть опциональными.

    """

    text: str | None
    caption: str | None

    from_user_id: int | None
    from_user_full_name: str | None
    from_user_is_premium: bool | None

    chat_id: int | None
    chat_title: str | None

    story: bool | None  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
    reply_markup: bool | None  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
    photo: List | None  # TODO: В данный момент поле зависит от aiogram, оставил так для обратной совместимости
    new_chat_members: bool | None  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
    external_reply: bool | None  # Для бизнес логики имеет значение только наличие или отсутствие этого поля
