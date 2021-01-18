import shlex
import sys
import time
import threading
import concurrent.futures
import socket
import utilities.logger as logger

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

        self.log = logger.Logger()

    def set_target(self, ip):
        try:
            self.log.info(f'Setting target to {ip}')
            self.target = socket.gethostbyname(ip)
        except:
            self.log.error('Invalid target IP format')
            return

    def set_latency(self, val):
        self.log.info(f'Setting latency to {val}')
        self.latency = val

    def set_workers(self, val):
        self.log.info(f'Setting max workers to {val}')
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
            self.log.error(f'We require more minerals... pardon, a target.')
            return
        
        start = time.perf_counter()
        self.log.info('Started port scanning')

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            _ = executor.map(self.run_scan, self.port_range)

        finish = time.perf_counter()

        self.log.info(f'Finised scanning {len(self.port_range)} port(s) in {round(finish-start, 2)} second(s)')

        return self.open_ports