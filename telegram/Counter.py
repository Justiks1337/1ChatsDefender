import time

from utils.patterns.singleton import Singleton


class Counter(Singleton):
    """
    Счетчик для вывода данных в /ping
    Singleton паттерн
    """

    def init(self):
        self.messages_deleted = 0
        self.messages_handled = 0
        self.start_time = time.time()
