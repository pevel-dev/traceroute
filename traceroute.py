import random
import socket
import struct
import time


class Traceroute:
    def __init__(self, icmp_type, socket_provider):
        self._icmp_type = icmp_type
        self._socket_provider = socket_provider

    def traceroute(self, destination, max_hops, n, timeout, size, sequence_number):
        if sequence_number is None:
            seq = 0
        else:
            seq = sequence_number
        for ttl in range(1, max_hops + 1):
            results = []
            for i in range(n):
                results.append(self._task(ttl, size, destination, timeout, seq, self._icmp_type))
                if sequence_number is not None:
                    seq += 1

            yield results

            if destination in set(map(lambda x: x[0] if x is not None else " ", results)):
                return

    def _get_icmp_packet(self, sequence_number, size, icmp_type):
        icmp_code = 0
        data = b'\x00' * size
        packet_id = random.randint(0, 65535)

        packet = struct.pack('!BBHHH', icmp_type, icmp_code, 0, packet_id, sequence_number) + data
        checksum = self._calculate_checksum(packet)

        return struct.pack('!BBHHH', icmp_type, icmp_code, checksum, packet_id, sequence_number) + data, packet_id

    def _task(self, ttl, size, destination, timeout, sequence_number, icmp):
        sock = self._socket_provider(ttl, timeout)
        packet, packet_id = self._get_icmp_packet(sequence_number, size, icmp)
        start_time = self._send_icmp(sock, packet, destination)
        response = self._receive_icmp(sock)
        sock.close()

        if response:
            return response[0], (response[1] - start_time) * 1000
        return None

    @staticmethod
    def _receive_icmp(sock):
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                return addr[0], time.time()
            except socket.timeout:
                return None

    @staticmethod
    def _calculate_checksum(data):
        checksum = 0
        for i in range(0, len(data), 2):
            checksum += (data[i] << 8) + data[i + 1]
        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum += (checksum >> 16)
        return (~checksum) & 0xffff

    @staticmethod
    def _send_icmp(sock, packet, destination):
        sock.sendto(packet, (destination, 0))
        return time.time()


class TracerouteIPv4:

    def __init__(self):
        self.traceroute = Traceroute(8, self._get_icmp_socket)

    def route(self, destination, max_hops, n, timeout=5, size=1, sequence_number=None):
        for i in self.traceroute.traceroute(destination, max_hops, n, timeout, size, sequence_number):
            yield i

    @staticmethod
    def _get_icmp_socket(ttl, timeout):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        sock.settimeout(timeout)

        return sock


class TracerouteIPv6:
    def __init__(self):
        self.traceroute = Traceroute(128, self._get_icmp_socket)

    def route(self, destination, max_hops, n, timeout=5, size=1, sequence_number=None):
        for i in self.traceroute.traceroute(destination, max_hops, n, timeout, size, sequence_number):
            yield i

    @staticmethod
    def _get_icmp_socket(ttl, timeout):
        sock = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_ICMPV6)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_UNICAST_HOPS, ttl)
        sock.settimeout(timeout)
        return sock
