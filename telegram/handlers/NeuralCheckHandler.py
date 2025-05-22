import logging
from abc import ABC, abstractmethod
import joblib
import os
import re

import pymorphy3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from utils import AbstractHandler, Singleton
from telegram.Message import Message
from telegram.punishments import warning
from dotenv import load_dotenv


load_dotenv()


class NeuralCheckHandler(AbstractHandler):

    async def handle(self, message: Message):
        neural_client = AIClient()

        # Я не хочу тратить токены в нейронке на маленькие сообщения. И писать отдельный хендлер под это не хочу. И вообще комментарий переводить на английский тоже лень
        if len(message.message.text.split(" ")) < 7:
            logging.debug("NeuralCheckHandler ignore message, because it len < 10")
            return await super().handle(message)

        if neural_client.check_message(message.message.text):
            message.is_trusted = False
            message.execute_middleware = True
            message.execute = warning(message.message)
            logging.info("NeuralCheckHandler worked now")
            return message

        return await super().handle(message)


class AIClientInterface(ABC):
    @abstractmethod
    def init(self, *args, **kwargs):
        pass

    @abstractmethod
    def check_message(self, text: str) -> bool:
        pass


class AIClient(Singleton, AIClientInterface):
    """
    HIGH RESOURCES CLASS! LOAD THIS IN main.py!

    tf-idf model for messages
    """

    def init(self, *args, **kwargs):

        # download filters
        nltk.download('stopwords')
        nltk.download('punkt_tab')
        nltk.download('punkt')

        # WARNING! HIGH RESOURCES OPERATIONS!
        self.__morph = pymorphy3.MorphAnalyzer()
        self.__model = joblib.load(os.getenv('MODEL_PATH'))
        self.__tfidf = joblib.load(os.getenv('TFIDF_PATH'))

        # uses in __clear_message for remove all special symbols
        self.__pattern = re.compile(r"[^a-zA-Zа-яА-Я0-9\s]")

        # stop_words
        self.__stop_words = set(stopwords.words('russian'))

    def check_message(self, text: str) -> bool:
        """
        Validate message using neural network API client

        :param text: text of message
        :return: bool. True if message not valid, else False
        """

        tfidf_message = self.__tfidf.transform([self.__clear_message(text)])

        result = self.__model.predict(tfidf_message)[0]

        # result can be "spam" or "true"
        return result == "spam"

    def __lemmatize(self, text):
        """
        Лемматизация текста - приведение слов к единой форме. Это требуется для удаления лишнего шума.
        :param text: Text of message
        :return: лемматизированный текст
        """
        lemmatized_words = [self.__morph.parse(word)[0].normal_form for word in text.split()]
        return " ".join(lemmatized_words)


    def __remove_stop_words(self, text):
        """
        Стоп слова это союзы, местоимения, слова не имеющие смысла и прочие.
        Удаление стоп слов приводит к уменьшению шума в модели
        :param text:
        :return:
        """
        words = word_tokenize(text, language='russian')
        filtered_words = [word for word in words if word.lower() not in self.__stop_words]
        return ' '.join(filtered_words)

    def __clear_message(self, text: str) -> str:
        """clear message process before checking"""

        # text to lower
        text = text.lower()

        # нормализация, приводим все ё к е, чтобы токенов в tf-idf было меньше
        text = text.replace('ё', 'е')

        # remove all special symbols
        text = self.__pattern.sub('', text)

        # remove stop words
        text = self.__remove_stop_words(text)

        # lemmatize words
        text = self.__lemmatize(text)

        return text
