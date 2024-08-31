import asyncio
import datetime

from dotenv import load_dotenv

from telegram.dispatcher import dp
from utils import DatabaseConnection
from telegram.router import Router


load_dotenv()


async def main():
    database_connection = DatabaseConnection()
    await database_connection.get_connection()  # Database is Singleton, that's why I call this method here
    Router()  # router - singleton. This line execute initial Router method

    import telegram.handlers  # load handlers
    await dp.start_polling(telegram.dispatcher.bot)


if __name__ == '__main__':
    import logging

    logger = logging.getLogger()
    logger.level = logging.DEBUG
    logging.basicConfig(filename="logs/{:%Y-%m-%d}.log".format(datetime.datetime.now()), level=logging.DEBUG)

    asyncio.run(main())
