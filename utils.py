import socket


def get_ip_from_host(host: str) -> str | None:
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        return None
    return ip


def get_host_from_ip(ip: str) -> str | None:
    try:
        host = socket.gethostbyaddr(ip)
    except socket.herror:
        return None
    return host[0]
