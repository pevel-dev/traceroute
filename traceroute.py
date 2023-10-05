import time

from icmp import send_icmp_packet, receive_icmp_response
from utils import get_host_from_ip


def traceroute(destination_ip, max_ttl, timeout):
    for ttl in range(1, max_ttl + 1):
        send_icmp_packet(destination_ip, ttl)
        response, address = receive_icmp_response(timeout)
        if address:
            host = get_host_from_ip(address[0])
            print(f"{ttl}: {address[0]} ({host})")
        else:
            print(f"{ttl}: *")

        if address and address[0] == destination_ip:
            print("Достигнут конечный узел.")
            break
        time.sleep(0.1)
