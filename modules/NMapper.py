# ToDo: integrate with nmap to scan open ports

# # find nmap
# cmd = "which nmap"
# args = shlex.split(cmd)
# sub_proc = subprocess.Popen(args, stdout=subprocess.PIPE)
# output, errs = sub_proc.communicate(timeout=10)

# n_path = output.decode('utf8').strip()
# print(n_path)

# # nmap version
# nmap = n_path
# cmd = f'{nmap} --version'
# args = shlex.split(cmd)
# sub_proc = subprocess.Popen(args, stdout=subprocess.PIPE)
# output, errs = sub_proc.communicate(timeout=10)
# print(output.decode('utf8').strip())

class Nmap:
    def __init__(self):
        self.ports = None