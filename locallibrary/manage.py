#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import socket
from threading import Thread

from health_check_server.Protocol import *
import psutil


def get_data():
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    error_flag = "0"
    msg = cpu_percent + "|" + ram_percent + "|" + error_flag

    return msg


def server():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('127.0.0.1', 8080))
    serv.listen(5)

    while True:
        conn, addr = serv.accept()

        data = get_data()

        conn.send(bytes(data))

        conn.close()
        print('client disconnected')


def main():
    """health check run thread"""
    # health_thread = Thread(target=server)
    # health_thread.start()

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locallibrary.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
