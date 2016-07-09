MCAST_IP = "228.0.0.5"
MCAST_PORT = 9999
MCAST_ADDR = (MCAST_IP, MCAST_PORT)


def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]
