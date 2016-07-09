MCAST_IP = "228.0.0.5"
MCAST_PORT = 9999
MCAST_ADDR = (MCAST_IP, MCAST_PORT)
BROKER_1_PORT = 10000
BROKER_2_PORT = 10001


def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]
