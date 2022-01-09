import socket
from Protocol import *

data_log_wrapper = "<----data---->\n"
error_log_wrapper = "<----error---->\n"


def health_check():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))
    client.send(b"1")
    from_server = client.recv(4096)
    client.close()

    stats = decode_msg(from_server)
    error_flag = stats[-1]
    stats = stats[:-1]

    log_data = format_data(error_flag != "0", error_flag, stats)

    with open("statistics.log", "w") as log:
        log.write(log_data)

    print(from_server)


def format_data(error, error_msg, *stats):
    if error:
        return error_log_wrapper + error_msg + error_log_wrapper
    else:
        msg = ""
        stat_list = ["CPU", "RAM"]
        for count, stat in enumerate(stats):
            msg += stat_list[count] + ": " + stat

        return data_log_wrapper + msg + data_log_wrapper
