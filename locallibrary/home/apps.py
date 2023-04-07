from django.apps import AppConfig
import socket
from threading import Thread
import psutil

from . import Protocol

import mysql.connector


def get_data():
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent

    error_flag = "0"
    stats = [cpu_percent, ram_percent, error_flag]

    msg = Protocol.encode_msg(stats)

    return msg


def server():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('0.0.0.0', 8080))
    serv.listen(5)

    while True:
        conn, addr = serv.accept()

        data = get_data()

        conn.send(data)

        conn.close()
        # print('client disconnected')


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        from .recommendation_engiene import CycleThread
        """run background threads when ready"""
        """health check run thread"""
        health_thread = Thread(target=server)
        health_thread.setDaemon(True)
        health_thread.start()

        """run cycle process to determine users interests"""
        cycle = CycleThread()
        recommendation_cycle = Thread(target=cycle.start)
        recommendation_cycle.setDaemon(True)
        recommendation_cycle.start()
