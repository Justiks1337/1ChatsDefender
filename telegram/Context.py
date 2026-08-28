from telegram.MessageData import MessageData


class Context:

    """
    Instances of this class will go through a chain of checks

    Context attrs:

    message: telegram.MessageData - датакласс содержащий нужную для чеков информацию о сообщении
    execute: coroutine - coro, which will be called in any case after passing the chain of checks, default - None
    is_trusted: bool - has the message passed verification
    """

    def __init__(self, message: MessageData):
        self.__message: MessageData = message
        self._execute = None
        self._is_trusted = True
        self._execute_middleware = False
        self._next_handler = True

    @property
    def message(self):
        return self.__message

    @property
    def execute(self):
        return self._execute

    @execute.setter
    def execute(self, value):
        self._execute = value

    @property
    def is_trusted(self):
        return self._is_trusted

    @is_trusted.setter
    def is_trusted(self, value: bool):
        self._is_trusted = value

    @property
    def execute_middleware(self):
        return self._execute_middleware

    @execute_middleware.setter
    def execute_middleware(self, value: bool):
        self._execute_middleware = value

    @property
    def next_handler(self):
        return self._next_handler

    @next_handler.setter
    def next_handler(self, value):
        self._next_handler = value
