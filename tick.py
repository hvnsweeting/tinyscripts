#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tick then run cmd

better alternative to sleep N && cmd2
"""
import os
import sys
import subprocess
import time


def clear_screen():
    subprocess.call(['cls'] if os.name == 'nt' else ['clear'])


seconds_remain = int(sys.argv[1])
while seconds_remain > 0:
    clear_screen()
    print('{}'.format(seconds_remain))
    time.sleep(1)
    seconds_remain -= 1

subprocess.call(sys.argv[2:])
