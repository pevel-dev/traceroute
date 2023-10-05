import argparse

from traceroute import traceroute
from utils import get_ip_from_host

parser = argparse.ArgumentParser(description="traceroute")
parser.add_argument('--host', type=str, help='Host', default="google.com")
parser.add_argument('--ttl', type=int, help='Max ttl', default=30)
parser.add_argument('--timeout', type=int, help='Timeout in seconds', default=2)


if __name__ == "__main__":
    args = parser.parse_args()

    destination_ip = get_ip_from_host(args.host)
    if not destination_ip:
        print("Not found host")

    traceroute(destination_ip, args.ttl, args.timeout)
