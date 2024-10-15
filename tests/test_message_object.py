# virtualization real messages from aiogram


class TestAiogramMessage:
    def __init__(self,
                 text="simple text",
                 chat_id=-1002168533309,
                 new_chat_members=False,
                 user_id=None,
                 is_premium=True
                 ):
        self.text = text
        self.chat = Chat(chat_id)
        self.new_chat_members = new_chat_members

        if user_id:
            self.from_user = TestAiogramUser(is_premium, user_id)
        else:
            self.from_user = TestAiogramUser(is_premium)


class TestAiogramUser:
    def __init__(self, is_premium, user_id=2121622736):
        self.id = user_id
        self.is_premium = is_premium


class Chat:
    def __init__(self, chat_id: int):
        self.id = chat_id
