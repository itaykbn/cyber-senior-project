import socket
import time

import requests

from .Protocol import *
import mysql.connector

data_log_wrapper = "<----data---->\n"
error_log_wrapper = "<----error---->\n"


def ping_db(db):
    if db == "sql":
        try:
            cnx = mysql.connector.connect(
                user="docker",
                password="docker",
                host="localhost",
                port=3306,
                database="mngmnt")

            if cnx.is_connected():
                cnx.close()
                return "UP"
            else:
                cnx.close()
                return "DOWN"
        except:
            return "DOWN"
    else:
        try:
            res = requests.get('http://127.0.0.1:8123')

            if res.status_code == 200:
                return "UP"
            else:
                return "DOWN"
        except:
            return "DOWN"


def health_check():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('10.100.102.3', 8080))
        client.send(b"1")
        from_server = client.recv(4096)
        client.close()

        stats = decode_msg(from_server)
        # print(stats)
        error_flag = stats[-1]
        stats = stats[:-1]

        log_data = format_data(error_flag != "0", error_flag, stats)

        with open("statistics.log", "a") as log:
            log.write(log_data)

        return log_data
    except:
        return f"{error_log_wrapper}server down\n{error_log_wrapper}"


def format_data(error, error_msg, stats):
    if error:
        return error_log_wrapper + error_msg + error_log_wrapper
    else:
        msg = ""
        stat_list = ["CPU", "RAM", "MYSQL"]
        for count, stat in enumerate(stats):
            # print(stat)
            msg += f"{stat_list[count]}:{stat}\n"

        return f"{data_log_wrapper}{msg}{data_log_wrapper}"


def get_db_status():
    try:
        return f"MYSQL:{ping_db('sql')}\nCLICKHOUSE:{ping_db('click')}"
    except Exception as e:
        print(e)
        return "oof"


if __name__ == '__main__':
    while True:
        server_health = health_check()
        db_health = get_db_status()

        print(f"====SERVER====\n{server_health}====SERVER====\n====DB====\n{db_health}\n====DB====\n")
        time.sleep(4)
