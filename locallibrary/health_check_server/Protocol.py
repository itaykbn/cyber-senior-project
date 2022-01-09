def encode_msg(*stats):
    msg = ""
    for stat in stats:
        msg += str(stat)
        msg += "|"
    msg = msg[:-1]

    return bytes(msg)


def decode_msg(msg):
    msg = msg.decode("utf-8")
    stats = msg.split("|")

    return stats
