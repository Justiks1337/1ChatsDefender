import time

from utils.patterns.singleton import Singleton


class Counter(Singleton):
    """Хранит статистику работы бота для вывода в команде /ping.

    Использует паттерн Singleton: счётчики и время запуска хранятся
    в единственном экземпляре класса.
    """

    def init(self):
        self.messages_deleted = 0
        self.messages_handled = 0
        self.start_time = time.time()
