import shlex
import sys
import time
import threading
import concurrent.futures
import socket

class Port:
    def __init__(self):
        self.number = 0
        self.status = 'closed'
        # ToDo: Maybe integrate with nmap class to save information like service running on port and version

class PortScanner:
    def __init__(self):
        self.target = None
        self.port_range = range(1,65535)
        self.open_ports = {}
        self.latency = 0.3
        self.workers = 1000

    def set_target(self, ip):
        try:
            print(f'[-] Setting target to {ip}')
            self.target = socket.gethostbyname(ip)
        except:
            print('[!] Invalid target IP format')
            return

    def set_latency(self, val):
        print(f'[-] Setting latency to {val}')
        self.latency = val

    def set_workers(self, val):
        print(f'[-] Setting max workers to {val}')
        self.workers = val

    def run_scan(self, port):
        socket.setdefaulttimeout(self.latency)
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        target_port = Port()
        target_port.number = port

        try:
            connection = soc.connect((self.target, target_port.number))
            target_port.status = 'Open'
            self.open_ports[target_port.number] = target_port.status
            connection.close()
        except (ConnectionRefusedError, AttributeError, OSError):
            pass

    def scan_ports(self):
        if self.target is None:
            print(f'We require more minerals... pardon, a target.')
            return
        
        start = time.perf_counter()
        print('[-] Started port scanning')

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            _ = executor.map(self.run_scan, self.port_range)

        finish = time.perf_counter()

        print(f'[-] Finised scanning {len(self.port_range)} port(s) in {round(finish-start, 2)} second(s)')

        return self.open_ports