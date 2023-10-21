import argparse
from tabulate import tabulate

from traceroute import TracerouteIPv6, TracerouteIPv4
from utils import get_ip_from_host, get_host_from_ip, get_ipv6_addr_from_host

parser = argparse.ArgumentParser(description="traceroute")
parser.add_argument('--host', type=str, help='Host', default="ya.ru")
parser.add_argument('--ttl', type=int, help='Max ttl', default=30)
parser.add_argument('--timeout', type=float, help='Timeout float', default=2.0)
parser.add_argument('--seq', type=int, help='Seq num', default=0)
parser.add_argument('--size', type=int, help='Num of bytes size', default=60)
parser.add_argument('-n', type=int, help='Count packets send', default=3)
parser.add_argument('--ipv', type=int, help='ip version', default=4)


def build_provider_traceroute(host, ipv):
    if ipv == 4:
        return get_ip_from_host(host), TracerouteIPv4()
    elif ipv == 6:
        return get_ipv6_addr_from_host(host), TracerouteIPv6()
    else:
        raise ValueError('Invalid ip version')


def out_traceroute_result(traceroute_provider, args, destination_ip):
    print(f'Traceroute to {args.host} ({destination_ip}). Send {args.n} packets for {args.size} bytes each')

    for i, result in enumerate(
            traceroute_provider.route(destination_ip, args.ttl, args.n, args.timeout, args.size, args.seq), 1):
        current_result = [f'{i:2d}:']
        ips = set()
        for r in result:
            if r:
                ip, time = r
                ips.add(ip)
                current_result.append(f"{ip} ({get_host_from_ip(ip)}) {time:.3f} ms")
            else:
                current_result.append("*")

        print(' '.join(current_result))

        if destination_ip in ips:
            print('Достигнут конечный узел.')
            break


if __name__ == "__main__":
    args = parser.parse_args()

    destination_ip, traceroute = build_provider_traceroute(args.host, args.ipv)
    if not destination_ip:
        print("Not found host")
        quit(0)
    out_traceroute_result(traceroute, args, destination_ip)
