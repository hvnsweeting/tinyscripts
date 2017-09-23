#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Send notification when there are processes use more than THRESHOLD MiB
of memory
Tested on Python 3.5, Ubuntu 16.04
'''
import argparse
import logging
import os
import subprocess as spr

from collections import defaultdict

import psutil

logging.basicConfig(filename=os.path.expanduser("~/.palert.log"),
                    level=logging.INFO,
                    format="%(asctime)s:" + logging.BASIC_FORMAT
                    )

logger = logging.getLogger('palert')

argp = argparse.ArgumentParser()
argp.add_argument("threshold", default=1024, type=int, nargs='?')
args = argp.parse_args()

THRESHOLD = args.threshold

msgs = []
name_sizes = defaultdict(int)

for process in psutil.process_iter():
    rss = process.memory_info().rss
    size_in_mib = rss / 1024 / 1024

    # TODO
    # this is wrong when we run python scripts, they will all add up
    # but okay for now
    # read process.name?? for more detail why use first 15 chars
    name = process.name().split()[0][:15]
    name_sizes[name] += size_in_mib

for name, size in name_sizes.items():
    if size > THRESHOLD:
        msg = "{}: {} MiB".format(name, size)
        msgs.append(msg)

if msgs:
    notification = '\t'.join(msgs)
    # If call from cron, must set DISPLAY so notify-send knows where to send
    import os
    os.environ['DISPLAY'] = ':0'
    logger.info(notification)
    spr.call(['/usr/bin/notify-send', notification])
else:
    logger.debug('No process that consumes lot of memory')
