# XPOSD

Pronounced /ikˈsplōdəd/ (exposed) is a tool I'm working on to automate most of the RECON part of Hacking.

## Usage
```
python3 xposd.py [-h] --target  [--latency] [--workers]
```
Examples:
```
python3 xposd.py -t 10.10.10.10  
python3 xposd.py -t 10.10.10.10 -l 1
python3 xposd.py -t 10.10.10.10 -w 1000 -l 0.5
```

## Plans
- Integrate with Nmap for detailed scan of specifically open ports
- Integrate / Implement directory discovery on http services
- ... find more ideas ... 

# Licence
It's free, have fun, just don't do dumb stuff... hack for good.