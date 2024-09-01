# virtualization real messages from aiogram


class TestAiogramMessage:
    def __init__(self,
                 text="simple text",
                 chat_id=-1002168533309,
                 new_chat_members=False,
                 user_id=None,
                 is_premium=False
                 ):
        self.text = text
        self.chat = Chat(chat_id)
        self.new_chat_members = new_chat_members
        self.is_premium = is_premium

        if user_id:
            self.from_user = TestAiogramUser(user_id)
        else:
            self.from_user = TestAiogramUser()


class TestAiogramUser:
    def __init__(self, user_id=2121622736):
        self.id = user_id


class Chat:
    def __init__(self, chat_id: int):
        self.id = chat_id
