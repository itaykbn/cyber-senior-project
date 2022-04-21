import threading
from clickhouse_driver import Client
from datetime import datetime

from threading import Thread, Timer, Event


class Queue:
    def __init__(self):
        self.__max_length = 1000000
        self.__queue = []

    def enqueue(self, item):
        if len(self.__queue) < self.__max_length:
            self.__queue.append(item)

    def dequeue(self):
        return self.__queue.pop(0)

    def is_empty(self):
        return len(self.__queue) == 0


class Singleton(object):
    __lock = threading.Lock()
    __instance = None

    @classmethod
    def instance(cls):
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    cls.__instance = cls()
        return cls.__instance


class MyThread(Thread):
    def __init__(self, event, function):
        Thread.__init__(self)
        self.stopped = event
        self.func = function

    def run(self):
        while not self.stopped.wait(0.5):
            self.func()


class ClickHouseService(Singleton):
    def __init__(self):
        self.__queue = Queue()
        # self.scheduler = sched.scheduler(time.time, time.sleep)
        self.__repeat = 10

        self.__client = Client('localhost',
                               user='itay',
                               password='pronto',
                               database='Analytics'
                               )
        self.__start()

    def __start(self):
        print("my hood is showing")

        stop_flag = Event()

        thread = MyThread(stop_flag, self.__handle_queue)

        thread.start()

    def _print(self):
        print("hello")

    def __handle_queue(self):
        print(f"my hoodness {datetime.now()}")
        if not self.__queue.is_empty():
            while not self.__queue.is_empty():
                query = self.__queue.dequeue()
                self.__exec_query(query)

    def __exec_query(self, query):
        return self.__client.execute(query)

    def execute(self, query):
        print("--------------------query : " + query)
        return self.__queue.enqueue(query)
