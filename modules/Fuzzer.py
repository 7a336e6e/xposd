import os.path

class Directory:
    def __init__(self):
        self.target = None
        self.ports = None
        self.wordlist = '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt'

    def set_target(self, ip):
        self.target = ip
    
    def set_ports(self, ports):
        self.ports = ports
    
    def set_wordlist(self, wl_path):
        if path.exists(wl_path):
            self.wordlist = wl_path
        else:
            print(f'[!] Provided wordlist path ({wl_path}) does not exist on current system, fallback to default wl({self.wordlist})')