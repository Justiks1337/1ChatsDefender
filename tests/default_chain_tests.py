import unittest

from telegram.Message import Message
from telegram.chains.DefaultChain import DefaultChain
from telegram.handlers.IsGroupHandler import IsGroupHandler
from telegram.handlers.MessageHasTextHandler import MessageHasTextHandler
from telegram.handlers.IsAdminHandler import IsAdminHandler, ChatAdminsFabric, AdministratorsCache
from telegram.handlers.IsJoinMessageHandler import IsJoinMessageHandler
from telegram.handlers.CheckBanwordsHandler import CheckBanwordsHandler
from tests.test_message_object import TestAiogramMessage
from tests.test_handler import TestHandler


MAGIC_USER_ID = 2121622736  # Developer id
MAGIC_GROUP_ID = -1002168533309  # id of group "Чат защитника"


class IsGroupHandlerTest(unittest.IsolatedAsyncioTestCase):
    async def test_without_triggers(self):
        message = Message(TestAiogramMessage())

        testable_handler = IsGroupHandler()
        test_handler = TestHandler()  # Если тест пройден, то этот хендлер сработает. Если хендер не сработает, то вернет False - тест автоматически будет провален

        testable_handler.set_next(test_handler)

        self.assertFalse(await testable_handler.handle(message))

    async def test_with_triggers(self):
        message = Message(TestAiogramMessage(chat_id=MAGIC_USER_ID))
        # r = await DefaultChain().handle(message)  # Не имеет смысла, т.к. сообщение в цепочке не видоизменяется

        testable_handler = IsGroupHandler()
        test_handler = TestHandler()  # Если тест пройден, то этот хендлер не сработает. Если хендер сработает, то вернет False - тест автоматически будет провален

        testable_handler.set_next(test_handler)

        self.assertTrue(await testable_handler.handle(message))


class MessageHasTextHandlerTest(unittest.IsolatedAsyncioTestCase):
    async def test_without_triggers(self):
        message = Message(TestAiogramMessage())

        testable_handler = IsGroupHandler()
        test_handler = TestHandler()  # Если тест пройден, то этот хендлер сработает. Если хендер не сработает, то вернет False - тест автоматически будет провален

        testable_handler.set_next(test_handler)

        self.assertFalse(await testable_handler.handle(message))

    async def test_with_triggers(self):
        message = Message(TestAiogramMessage(text=None))
        # r = await DefaultChain().handle(message)  # Не имеет смысла, т.к. сообщение в цепочке не видоизменяется

        testable_handler = MessageHasTextHandler()
        test_handler = TestHandler()  # Если тест пройден, то этот хендлер не сработает. Если хендер сработает, то вернет False - тест автоматически будет провален

        testable_handler.set_next(test_handler)

        self.assertTrue(await testable_handler.handle(message))


class IsAdminHandlerTest(unittest.IsolatedAsyncioTestCase):
    async def test_without_triggers(self):
        message = Message(TestAiogramMessage(user_id=1))

        testable_handler = IsGroupHandler()
        test_handler = TestHandler()  # Если тест пройден, то этот хендлер сработает. Если хендер не сработает, то вернет False - тест автоматически будет провален

        testable_handler.set_next(test_handler)

        self.assertFalse(await testable_handler.handle(message))

    async def test_with_triggers(self):
        message = Message(TestAiogramMessage(user_id=MAGIC_USER_ID))
        # r = await DefaultChain().handle(message)  # Не имеет смысла, т.к. сообщение в цепочке не видоизменяется

        testable_handler = IsAdminHandler()
        test_handler = TestHandler()  # Если тест пройден, то этот хендлер не сработает. Если хендер сработает, то вернет False - тест автоматически будет провален

        admins_fabric = ChatAdminsFabric()
        admins_cache = AdministratorsCache([MAGIC_USER_ID])
        admins_fabric.cached_chat_administrators[MAGIC_GROUP_ID] = admins_cache

        testable_handler.set_next(test_handler)

        self.assertTrue(await testable_handler.handle(message))


class IsJoinMessageHandlerTest(unittest.IsolatedAsyncioTestCase):
    async def test_without_triggers(self):
        message = Message(TestAiogramMessage(new_chat_members=False))
        r = await DefaultChain().handle(message)
        self.assertEqual(message, r)
        r2 = await IsJoinMessageHandler().handle(message)
        self.assertTrue(r2.is_trusted)

    async def test_with_triggers(self):
        message = Message(TestAiogramMessage(new_chat_members=True))
        r = await DefaultChain().handle(message)
        self.assertFalse(r.is_trusted)
        r2 = await IsJoinMessageHandler().handle(message)
        self.assertFalse(r2.is_trusted)


class CheckBanwordsHandlerTest(unittest.IsolatedAsyncioTestCase):
    async def test_without_triggers(self):
        message = Message(TestAiogramMessage())
        r = await DefaultChain().handle(message)
        self.assertEqual(message, r)
        r2 = await CheckBanwordsHandler().handle(message)
        self.assertTrue(r2.is_trusted)

    async def test_with_triggers(self):
        admins_fabric = ChatAdminsFabric()
        admins_cache = AdministratorsCache([MAGIC_USER_ID])
        admins_fabric.cached_chat_administrators[MAGIC_GROUP_ID] = admins_cache

        message = Message(TestAiogramMessage(text="бля", user_id=1))
        r = await DefaultChain().handle(message)
        self.assertFalse(r.is_trusted)
        r2 = await CheckBanwordsHandler().handle(message)
        self.assertFalse(r2.is_trusted)
