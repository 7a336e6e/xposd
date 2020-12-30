import shlex
import sys
import os
import subprocess
import re
import datetime
import time

import xml.etree.ElementTree as ET

class NMap:
    def __init__(self):
        self.ports = None
        self.target = None
        self.scan_output = None
        self.http_services = None

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
        print(f'[-] Using nmap (Version: {nmap_version})')
        self.epoch = datetime.datetime.now().timestamp()
        print(f'[-] Setting epoch to: {self.epoch}')

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
        os.remove(self.scan_output)

        # get all hostnames
        hostnames = tree.findall('.//hostnames/hostname')
        for host in hostnames:
            print(f'[-] found hostname: {host.attrib["name"]}')

        # get all ports
        ports = tree.findall('.//ports/port')
        print(f'[*] Ports information:')
        for port in ports:
            print(f'|_[*] Port: {port.attrib["portid"]}/{port.attrib["protocol"]}')
            for child in port:
                if child.tag == "service":
                    port_service = child.attrib["name"]
                    print(f'|  [-] Service: {port_service}')
                    if port_service == "http":
                        if self.http_services is None:
                            self.http_services = []
                        else:
                            self.http_services.append(port)
                    if 'product' in child.attrib:
                        print(f'|  [-] Software: {child.attrib["product"]}')
                    if 'version' in child.attrib:
                        print(f'|  [-] Version: {child.attrib["version"]}')

    def run_scan(self):
        if self.ports is None:
            print(f'[!] There are no ports to scan. Try increasing the latency using --latency param.')

        p = ''
        for port in self.ports:
            p += f'{port},'
        p = p[:-1]

        self.scan_output = f'.{self.epoch}.xml'
        cmd = f'{self.nmap} -sV -Pn -p{p} -T5 -oX {self.scan_output} {self.target}'
        print(f'[-] Running nmap command: {cmd}')
        args = shlex.split(cmd)
        sub_proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        output, errs = sub_proc.communicate()
        poll = sub_proc.poll()

        self.parse_output()