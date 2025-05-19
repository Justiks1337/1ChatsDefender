from telegram.middleware.MiddlewareInterface import MiddlewareInterface
from utils.database.connection import DatabaseConnection
from telegram.Message import Message


class MessageToDatabaseMiddleware(MiddlewareInterface):
    @classmethod
    async def execute(cls, message: Message) -> Message:
        if not message.is_trusted:
            connect = DatabaseConnection().connect

            await connect.execute("INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)", (
                message.message.text,
                message.message.from_user.id,
                message.message.date,
                message.message.from_user.full_name,
                message.message.from_user.username,
                message.message.from_user.language_code,
                message.message.from_user.is_premium,
                int(bool(message.message.forward_origin)),
                int(bool(message.message.reply_to_message))))

            await connect.commit()

        return message
