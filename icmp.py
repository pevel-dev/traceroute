import socket
import struct


def send_icmp_packet(destination_ip, ttl):
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    icmp_id = 12345
    icmp_seq = 1

    icmp_type = 8  # 8 для ICMP Echo Request (пинг)
    icmp_code = 0
    icmp_checksum = 0
    icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
    icmp_data = b""

    def calculate_checksum(data):
        checksum = 0
        for i in range(0, len(data), 2):
            w = (data[i] << 8) + data[i + 1]
            checksum += w
        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum = ~checksum & 0xFFFF
        return checksum

    icmp_checksum = calculate_checksum(icmp_header + icmp_data)

    icmp_header = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)

    icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    icmp_packet = icmp_header + icmp_data

    icmp_socket.sendto(icmp_packet, (destination_ip, 0))

    icmp_socket.close()


def receive_icmp_response(timeout):
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_socket.settimeout(timeout)

    try:
        response, address = icmp_socket.recvfrom(1024)
        icmp_header = response[20:28]
        icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq = struct.unpack("!BBHHH", icmp_header)

        if icmp_type == 0:  # Echo Reply
            return response, address
        elif icmp_type == 11:  # Time Exceeded
            return response, address
        else:
            return None, None
    except socket.timeout:
        return None, None
    finally:
        icmp_socket.close()
