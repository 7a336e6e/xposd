import shlex
import sys
import os
import subprocess
import re
import datetime
import time

import xml.etree.ElementTree as ET
import concurrent.futures

import utilities.logger as logger

class NMap:
    log = logger.Logger()

    def __init__(self):
        self.ports = None
        self.target = None
        self.scan_output = None
        self.http_services = None

        self.latency = 0.3
        self.workers = 1000

        self.version_scan = True
        self.syn_scan = True

        self.scripts='default,vuln'

        cmd = "which nmap"
        args = shlex.split(cmd)
        sub_proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        output, errs = sub_proc.communicate(timeout=10)

        n_path = output.decode('utf8').strip()
        self.nmap = n_path
        cmd = f'{self.nmap} --version'
        args = shlex.split(cmd)
        sub_proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        output, errs = sub_proc.communicate(timeout=10)
        nmap_version = re.search('\s*([\d.]+)', output.decode('utf8').strip()).group(1)
        self.log.info(f'Using nmap (Version: {nmap_version})')

    def set_latency(self, val):
        self.log.info(f'Setting latency to {val}')
        self.latency = val

    def set_workers(self, val):
        self.log.info(f'Setting max workers to {val}')
        self.workers = val

    def set_ports(self, ports):
        self.ports = ports
    
    def set_target(self, ip):
        self.target = ip

    def set_nse(self, scripts):
        self.scripts = scripts

    def get_http_services(self):
        return self.http_services
    
    def parse_output(self):
        tree = ET.parse(self.scan_output)
        root = tree.getroot()

        # cleanup the junk
        # os.remove(self.scan_output)

        # get all hostnames
        hostnames = tree.findall('.//hostnames/hostname')
        for host in hostnames:
            self.log.info(f'found hostname: {host.attrib["name"]}')

        # get all ports
        ports = tree.findall('.//ports/port')
        self.log.info(f'Ports information:')
        for port in ports:
            self.log.info(f'Port: {port.attrib["portid"]}/{port.attrib["protocol"]}')
            for child in port:
                if child.tag == "service":
                    port_service = child.attrib["name"]
                    self.log.info(f'Service: {port_service}')
                    if port_service == "http":
                        if self.http_services is None:
                            self.http_services = []
                        else:
                            self.http_services.append(port)
                    if 'product' in child.attrib:
                        self.log.info(f'Software: {child.attrib["product"]}')
                    if 'version' in child.attrib:
                        self.log.info(f'Version: {child.attrib["version"]}')

    def network_map(self, port):
        cmd = f'{self.nmap} -sV -sC -Pn --script=default,vuln -p{port} -T5 {self.target}'

        args = shlex.split(cmd)
        sub_proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        output, errs = sub_proc.communicate()
        poll = sub_proc.poll()

    def run_scan(self):
        if self.ports is None:
            self.log.error(f'There are no ports to scan. Try increasing the latency using --latency param.')

        # p = ''
        # for port in self.ports:
        #     p += f'{port},'
        # p = p[:-1]

        self.log.info(f'Running nmap scan on ports {self.ports}')
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            _ = executor.map(self.network_map, self.ports)

        self.scan_output = f'output/{self.target}.xml'
        cmd = f'{self.nmap} -sV -sC -Pn --script=default,vuln -p{p} -T5 -oA {self.target} {self.target}'
        self.log.info(f'Running nmap command: {cmd}')
        args = shlex.split(cmd)
        sub_proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        output, errs = sub_proc.communicate()
        poll = sub_proc.poll()

        self.parse_output()