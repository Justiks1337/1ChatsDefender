import asyncio

from dotenv import load_dotenv

from telegram.dispatcher import dp
from utils import DatabaseConnection


load_dotenv()


async def main():
    database_connections = DatabaseConnection()
    await database_connections.get_connection()  # Database is Singleton, that's why I call this method here

    import telegram.handlers  # load handlers
    await dp.start_polling(telegram)


if __name__ == '__main__':
    asyncio.run(main())
