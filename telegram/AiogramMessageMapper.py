from aiogram.types import Message as AiogramMessage

from telegram.MessageData import MessageData


class AiogramMessageMapper:
    """Преобразует сообщение aiogram в данные, необходимые цепочке проверок."""

    @staticmethod
    def map(message: AiogramMessage) -> MessageData:
        from_user = message.from_user

        return MessageData(
            text=message.text,
            caption=message.caption,
            from_user_id=from_user.id if from_user is not None else None,
            from_user_full_name=from_user.full_name if from_user is not None else None,
            from_user_is_premium=from_user.is_premium if from_user is not None else None,
            chat_id=message.chat.id,
            chat_title=message.chat.title,
            story=True if message.story is not None else None,
            reply_markup=True if message.reply_markup is not None else None,
            photo=message.photo,
            new_chat_members=True if message.new_chat_members else None,
            external_reply=True if message.external_reply is not None else None,
        )
