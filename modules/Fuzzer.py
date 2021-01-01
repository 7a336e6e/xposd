import os.path
import time
import threading
import concurrent.futures

class Directory:
    def __init__(self):
        self.target = None
        self.ports = None
        self.wordlist = '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt'

        self.workers = 1000

    def set_target(self, ip):
        self.target = ip
    
    def set_ports(self, ports):
        self.ports = ports

    def set_workers(self, val):
        self.workers = val
    
    def set_wordlist(self, wl_path):
        if path.exists(wl_path):
            self.wordlist = wl_path
        else:
            print(f'[!] Provided wordlist path ({wl_path}) does not exist on current system, fallback to default wl({self.wordlist})')

    def get_request(self, path):
        dir_path = path.replace("\n","")
        # ToDo: Implement requests for directory

    def run_dfuz(self):
        wl = open(self.wordlist, 'r').readlines()

        start = time.perf_counter()
        print('[-] Starting directory fuzzing')

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            _ = executor.map(self.get_request, wl)

        finish = time.perf_counter()

        print(f'[-] Finised directory fuzzing')
