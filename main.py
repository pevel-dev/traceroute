import argparse

from traceroute import Traceroute
from utils import get_ip_from_host, get_host_from_ip

parser = argparse.ArgumentParser(description="traceroute")
parser.add_argument('--host', type=str, help='Host', default="google.com")
parser.add_argument('--ttl', type=int, help='Max ttl', default=30)
parser.add_argument('--timeout', type=float, help='Timeout float', default=2.0)
parser.add_argument('--seq', type=int, help='Seq num', default=0)
parser.add_argument('--size', type=int, help='Num of bytes size', default=60)
parser.add_argument('-n', type=int, help='Count packets send', default=5)

if __name__ == "__main__":
    args = parser.parse_args()

    destination_ip = get_ip_from_host(args.host)
    if not destination_ip:
        print("Not found host")
        quit(0)
    print(f'Traceroute to {args.host} ({destination_ip}). Send {args.n} packets for {args.size} bytes each')
    i = 1
    for result in Traceroute().traceroute(destination_ip, args.ttl, args.n, args.timeout, args.size, args.seq):
        out = [f'{i}:']
        ips = set()
        for r in result:
            if r:
                ip, time = r
                if ip in ips:
                    continue
                ips.add(ip)
                out.append(f"{ip} ({get_host_from_ip(ip)}) {round(time, 3)} ms")
            else:
                out.append("*")
        print(' '.join(out))
        if destination_ip in ips:
            print('Достигнут конечный узел.')
        i += 1
