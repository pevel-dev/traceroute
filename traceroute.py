import socket
import struct
import time


class Traceroute:
    def traceroute(self, destination, max_hops, n, timeout=5, size=1, sequence_number=0):
        for ttl in range(1, max_hops + 1):
            results = []
            for i in range(n):
                results.append(self._task(ttl, size, destination, timeout, sequence_number))
            yield results

            if destination in set(map(lambda x: x[0] if x is not None else " ", results)):
                return

    def _get_icmp_packet(self, sock, sequence_number, size):
        icmp_type = 8
        icmp_code = 0
        data = b'\x00' * size
        packet_id = int(int((id(sock) / 65535)) & 0xFFFF)

        temp = struct.pack('!BBHHH', icmp_type, icmp_code, 0, packet_id, sequence_number) + data
        checksum = self._calculate_checksum(temp)

        return struct.pack('!BBHHH', icmp_type, icmp_code, checksum, packet_id, sequence_number) + data, packet_id

    def _task(self, ttl, size, destination, timeout, sequence_number):
        sock = self._get_icmp_socket(ttl)
        packet, packet_id = self._get_icmp_packet(sock, sequence_number, size)
        start_time = self._send_icmp(sock, packet, destination)

        sock = self._get_receive_socket(timeout)
        response = self._receive_icmp(sock, packet_id)
        sock.close()

        if response:
            return response[0], (response[1] - start_time) * 1000
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
        sock.close()
        return time.time()

    @staticmethod
    def _receive_icmp(sock, packet_id):
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                icmp_header = data[20:28]
                icmp_type, code, checksum, recv_id, sequence = struct.unpack('!BBHHH', icmp_header)
                if icmp_type == 0 or icmp_type == 11:
                    return addr[0], time.time()
            except socket.timeout:
                return None

    @staticmethod
    def _get_icmp_socket(ttl):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        return sock

    @staticmethod
    def _get_receive_socket(timeout):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(timeout)
        return sock
