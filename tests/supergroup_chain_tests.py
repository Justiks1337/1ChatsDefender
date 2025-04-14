import unittest

from telegram.Message import Message
from tests.test_message_object import TestAiogramMessage
from telegram.handlers.ManySpacesHandler import ManySpacesHandler
from telegram.handlers.HasPremiumEmojisHandler import HasPremiumEmojisHandler
from telegram.handlers.UpperCaseHandler import UpperCaseHandler


class ManySpacesHandlerTest(unittest.IsolatedAsyncioTestCase):
    async def test_without_triggers(self):
        message = Message(TestAiogramMessage(text="Привет, как у тебя дела? Я а блин точн ааа ага а 🐷"))
        r2 = await ManySpacesHandler().handle(message)
        self.assertTrue(r2.is_trusted)

    async def test_with_triggers(self):
        message = Message(TestAiogramMessage(text="П р и в е т  Я в о т  Д у м а ю  А как ты думаешь  С Т О и т  л и  н а м э э э э  ну например ну э э э э", user_id=1))
        r2 = await ManySpacesHandler().handle(message)
        self.assertFalse(r2.is_trusted)


class HasPremiumEmojisHandlerTest(unittest.IsolatedAsyncioTestCase):
    async def test_without_triggers(self):
        message = Message(TestAiogramMessage(text="Я думаю ну эээ ну ээээ ну эээ ну ээээ свинина хрю свинина хрю"))
        r2 = await HasPremiumEmojisHandler().handle(message)
        self.assertTrue(r2.is_trusted)

    async def test_with_triggers(self):
        message = Message(TestAiogramMessage(text="🐷🐷🐷🐷🐷🐷🐷🐷 амъъаъаъъаъъаъаххахахахахаха свинохряк :HEART:"))
        r2 = await HasPremiumEmojisHandler().handle(message)
        self.assertFalse(r2.is_trusted)


class UpperCaseHandlerTest(unittest.IsolatedAsyncioTestCase):

    async def test_without_triggers(self):
        message = Message(TestAiogramMessage(text="ААААаааааааААААааааааааааааааааааааа"))
        r2 = await UpperCaseHandler().handle(message)
        self.assertTrue(r2.is_trusted)

    async def test_with_triggers(self):
        message = Message(TestAiogramMessage(text="ААААААААААААААААААААААААААААААААААААААААААааааааа"))
        r2 = await UpperCaseHandler().handle(message)
        self.assertFalse(r2.is_trusted)