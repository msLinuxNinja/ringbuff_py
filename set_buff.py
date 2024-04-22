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

if arg == "eth0":
    interface = "eth0"
else:
    path = f"/sys{arg}/net"
    eth_dirs = glob.glob(os.path.join(path, 'eth*'))
    eth_dir = eth_dirs[0].replace("'","")
    interface = eth_dir.split('/')[-1]

if uptime_seconds < boot_threshold:
    subprocess.run(['/usr/bin/logger', '-t', logger_tag, '-i', f'Initial ring buffer setup for {interface}'])
    eth_stats = subprocess.check_output(['/usr/sbin/ethtool', '-g', interface]).decode().strip('\t')
    eth_cleaned = re.sub(r'\t', '', eth_stats)
    eth_lines = eth_cleaned.split('\n')
    subprocess.run(['/usr/bin/logger', '-t', logger_tag, '-i', f'{eth_lines[7]}, {eth_lines[10]}'])
else:
    subprocess.run(['/usr/bin/logger', '-t', logger_tag, '-i', f"Uhhohh something changed for {interface}"])
    eth_stats = subprocess.check_output(['/usr/sbin/ethtool', '-g', interface]).decode().strip('\t')
    eth_cleaned = re.sub(r'\t', '', eth_stats)
    eth_lines = eth_cleaned.split('\n')
    subprocess.run(['/usr/bin/logger', '-t', logger_tag, '-i', f'Current: {eth_lines[7]}, {eth_lines[10]}'])


if interface == "eth0":
    subprocess.run(['/usr/bin/logger', '-t', logger_tag, '-i', f"Setting up ring buffer for {interface}"])
    subprocess.run(['/usr/sbin/ethtool', '-G', interface, 'rx', '18139', 'tx', '2560'])
else:
    subprocess.run(['/usr/bin/logger', '-t', logger_tag, '-i', f"Setting up ring buffer for {interface}"])
    subprocess.run(['/usr/sbin/ethtool', '-G', interface, 'rx', '8192', 'tx', '8192'])