import asyncio
import logging

from dotenv import load_dotenv

from telegram.dispatcher import dp, bot
from utils import DatabaseConnection
from telegram.router import Router
from telegram.handlers.NeuralCheckHandler import AIClient
from telegram.Counter import Counter

load_dotenv()


@dp.startup()
async def startup(bot):
    database_connection = DatabaseConnection()
    await database_connection.get_connection()  # Database is Singleton, that's why I call this method here

    Router()  # router - singleton. This line executes initial Router method
    AIClient()  # high resources task, process it before bot start
    Counter()  # Is singleton. Init this for counter-start

    import telegram.handler  # load handlers


@dp.shutdown()
async def shutdown(bot):
    database_connection = DatabaseConnection()
    await database_connection.close()  # Закрываем соединение, для корректного завершнеия процесса


def setup_logging():
    file_log = logging.FileHandler('Log.log')
    console_out = logging.StreamHandler()

    logging.basicConfig(handlers=(file_log, console_out),
                        format='[%(asctime)s | %(levelname)s]: %(message)s',
                        datefmt='%m.%d.%Y %H:%M:%S',
                        level=logging.DEBUG)


if __name__ == '__main__':
    setup_logging()
    asyncio.run(dp.start_polling(bot))
