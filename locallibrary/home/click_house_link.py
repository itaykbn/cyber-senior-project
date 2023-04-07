import threading
from threading import Thread, Event

from clickhouse_driver import Client
from clickhouse_pool import ChPool


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


class MyThread(Thread):
    def __init__(self, event, function):
        Thread.__init__(self)
        self.stopped = event
        self.func = function

    def run(self):
        # print("i'm inside thread")
        while not self.stopped.wait(2):
            self.func()


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


class ClickHouseService(Singleton):

    def __init__(self):
        self.__queue = Queue()
        # self.scheduler = sched.scheduler(time.time, time.sleep)
        # self.__repeat = 10

        self.pool = ChPool(host="localhost",
                           user='itay',
                           password='pronto',
                           database='Analytics'
                           )

        self.__client = Client('localhost',
                               user='itay',
                               password='pronto',
                               database='Analytics'
                               )

        self.__start()

        self.lock = threading.Lock()

    def __start(self):
        stop_flag = Event()
        thread = MyThread(stop_flag, self.__handle_queue)
        thread.setDaemon(True)
        thread.start()

    def __handle_queue(self):
        if not self.__queue.is_empty():
            query_string = f"INSERT INTO Analytics.user_activity VALUES\n"

            while not self.__queue.is_empty():
                query = self.__queue.dequeue()
                query_string += query
                query_string += "\n"

            self.__exec_query(query_string)

    def __exec_query(self, query):
        with self.pool.get_client() as client:
            return client.execute(query)

    def execute(self, query):
        query_type = query.split("\n", 1)[0]

        if query_type == "SELECT":
            return self.__exec_query(query)

        else:
            self.__queue.enqueue(query)
            return None

    @staticmethod
    def insert(user_id, post_id, category, like, step_in):
        query_string = f"('{user_id}','{post_id}','{category}','{like}','{step_in}')"

        return query_string

    @staticmethod
    def select(from_table, where=None, select_list=None, group_by_list=None, order_by_list=None, limit_list=None):
        # select
        query_string = "SELECT\n"

        if select_list:
            query_string += ClickHouseService.__chain_list(select_list)
        else:
            query_string += "*"

        # from
        query_string += f"\nFROM {from_table} final\n"

        # where

        if where:
            query_string += "\nWHERE\n"
            query_string += where
        # group by

        if group_by_list:
            query_string += "\nGROUP BY\n"
            query_string += ClickHouseService.__chain_list(group_by_list)

        # order_by

        if order_by_list:
            query_string += "\nORDER BY\n"
            query_string += ClickHouseService.__chain_list(group_by_list)

        # limit

        if limit_list:
            query_string += f"\nLIMIT {limit_list[0]} BY {limit_list[1]}"

        return query_string

    @staticmethod
    def __chain_list(_list):
        _str = ""
        for item in _list:
            _str += item
            _str += ",\n"
        return _str[:-2]


def test():
    click = ClickHouseService()
    query_string1 = click.select("Analytics.user_activity",
                                 select_list=["user_id", "category", "sum(likes) AS likes, sum(step_in) AS step"],
                                 group_by_list=["user_id", "category"])
    query_string2 = click.insert("user_A", "post_A", "A", 0, 1)

    result2 = click.execute(query_string2)
    result2 = click.execute(query_string2)
    result2 = click.execute(query_string2)
    result2 = click.execute(query_string2)
    result2 = click.execute(query_string2)

    if result2:
        print(f"============= {result2}")
    else:
        print("no result")

# test()
