import asyncio
import argparse
import multiprocessing

from modules.PortScanner import PortScanner as PortScanner

parser = argparse.ArgumentParser(description='Process arguments for script')
parser.add_argument('--target', '-t', metavar='', help='(required) Target IP or Hostname (wihout http://)', required=True)
parser.add_argument('--latency', '-l', metavar='', type=float, help='(optional) Time to wait for Socket connection. Default value 0.5 seconds', required=False)
parser.add_argument('--workers', '-w', metavar='', type=int, help='(optional) Number of concurrent workers. Default value 1000', required=False)
# this argument is not used at anything yet ... I have some ideas
parser.add_argument('--port', '-p', metavar='', type=int, help='(optional) Use this value to start a scan for a single port', required=False)
args =parser.parse_args()

def main(args):
    print(args)

    port_scanner = PortScanner()
    port_scanner.set_target(args.target)

    if args.workers is not None:
        port_scanner.workers = args.workers

    if args.latency is not None:
        port_scanner.set_latency(args.latency)

    open_ports = port_scanner.scan_ports()
    print(open_ports)

if __name__ == '__main__':
    main(args)