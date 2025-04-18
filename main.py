import asyncio

from dotenv import load_dotenv

from telegram.dispatcher import dp
from utils import DatabaseConnection
from telegram.router import Router


load_dotenv()


async def main():
    database_connection = DatabaseConnection()
    await database_connection.get_connection()  # Database is Singleton, that's why I call this method here
    Router()  # router - singleton. This line execute initial Router method

    import telegram.handler  # load handlers
    await dp.start_polling(telegram.dispatcher.bot)


if __name__ == '__main__':
    import logging

    file_log = logging.FileHandler('Log.log')
    console_out = logging.StreamHandler()

    logging.basicConfig(handlers=(file_log, console_out),
                        format='[%(asctime)s | %(levelname)s]: %(message)s',
                        datefmt='%m.%d.%Y %H:%M:%S',
                        level=logging.DEBUG)

    asyncio.run(main())
