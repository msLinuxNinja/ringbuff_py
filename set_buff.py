#!/usr/bin/env python3

import sys
import subprocess
import re
import glob
import os

arg = sys.argv[1]

with open('/proc/uptime', 'r') as f:
    uptime_seconds = float(f.readline().split()[0])

boot_threshold = 300
logger_tag = "udev_an"

def set_interface(eth_if):
    if eth_if == "eth0":
        subprocess.run(['/usr/bin/logger', '-t', logger_tag, '-i', f"Setting up ring buffer for {eth_if}"])
        subprocess.run(['/usr/sbin/ethtool', '-G', eth_if, 'rx', '18139', 'tx', '2560'])
    else:
        subprocess.run(['/usr/bin/logger', '-t', logger_tag, '-i', f"Setting up ring buffer for {eth_if}"])
        subprocess.run(['/usr/sbin/ethtool', '-G', eth_if, 'rx', '8192', 'tx', '8192'])

def show_eth_stats(eth_if):
    eth_stats = subprocess.check_output(['/usr/sbin/ethtool', '-g', eth_if]).decode().strip('\t')
    eth_cleaned = re.sub(r'\t', '', eth_stats)
    eth_lines = eth_cleaned.split('\n')
    subprocess.run(['/usr/bin/logger', '-t', logger_tag, '-i', f'{eth_if}:{eth_lines[7]}, {eth_lines[10]}'])

if arg == "eth0":
    interface = "eth0"
else:
    path = f"/sys{arg}/net"
    eth_dirs = glob.glob(os.path.join(path, 'eth*'))
    eth_dir = eth_dirs[0].replace("'","")
    interface = eth_dir.split('/')[-1]

if uptime_seconds < boot_threshold:
    subprocess.run(['/usr/bin/logger', '-t', logger_tag, '-i', f'Initial ring buffer setup for {interface}'])
    show_eth_stats(interface)
    set_interface(interface)
    show_eth_stats(interface)
else:
    subprocess.run(['/usr/bin/logger', '-t', logger_tag, '-i', f"Uhhohh something changed for {interface}"])
    show_eth_stats(interface)
    set_interface(interface)
    show_eth_stats(interface)