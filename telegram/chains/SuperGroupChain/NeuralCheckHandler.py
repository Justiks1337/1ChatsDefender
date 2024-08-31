from abc import ABC, abstractmethod
import json as json_lib
import time
import os

from aiohttp import ClientSession
from utils import AbstractHandler, Singleton
from telegram.Message import Message
from telegram.punishments import ban


class NeuralCheckHandler(AbstractHandler):

    async def handle(self, message: Message):
        neural_client = APIClient()

        # Я не хочу тратить токены в нейронке на маленькие сообщения. И писать отдельный хендлер под это не хочу. И вообще комментарий переводить на английский тоже лень
        if len(message.message.text.split(" ")) < 10:
            return super().handle(message)

        if await neural_client.check_message(message.message.text):
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = ban(message.message)
            return message

        return super().handle(message)


class APIClientInterface(ABC):
    @abstractmethod
    def init(self, *args, **kwargs):
        pass

    @abstractmethod
    def check_message(self, text: str) -> bool:
        pass


class APIClient(Singleton, APIClientInterface):
    chat_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    revoke_token_url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    rquid = os.getenv("RQUID")
    authorization = os.getenv("GIGACHAT_API_AUTHORIZATION")

    def init(self, *args, **kwargs):
        self.__token_expires_at = 0
        self.__access_token = ""

    async def check_message(self, text: str) -> bool:
        """
        Validate message using neural network API client

        :param text: text of message
        :return: bool. True if message not valid, else False
        """

        if time.time() >= self.__token_expires_at:
            await self.__revoke_token()

        async with ClientSession() as session:
            async with session.post('https://gigachat.devices.sberbank.ru/api/v1/chat/completions',
                                    data=json_lib.dumps({"model": "GigaChat", 'messages': [{"role": "system",
                                                                                 "content": "я буду присылать тебе сообщения из чата, ты должен отвечать да или нет: да, если в сообщении есть заработок, нет если нет"},
                                                                                {"role": "user",
                                                                                 "content": text}],
                                          "n": 1, "stream": False, "max_tokens": 512,
                                          "repetition_penalty": 1, "update_interval": 0}),
                                    headers={"Authorization": f"Bearer {self.__access_token}",
                                             "Content-type": "application/json",
                                             "Accept": "application/json"}) as response:
                json = await response.json()
                return "да" in json["choices"][0]["message"]["content"].lower()

    async def __revoke_token(self):
        """
        Revoke authtoken, if it expired

        :return: None
        """

        async with ClientSession() as session:
            async with session.post('https://ngw.devices.sberbank.ru:9443/api/v2/oauth',
                                    headers={"Content-type": "application/x-www-form-urlencoded",
                                             "Accept": "application/json",
                                             "RqUID": APIClient.rquid,
                                             "Authorization": APIClient.authorization},
                                    data={"scope": "GIGACHAT_API_PERS"}) as response:
                json = await response.json()
                self.__token_expires_at = json['expires_at']
                self.__access_token = json['access_token']