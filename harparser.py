#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
Script for parsing Firefox HAR file.
'''

import sys
import json


def main():
    js = json.load(open(sys.argv[1]))
    l = js['log']
    entries = l['entries']
    simple_entries = [(entry['time'],
                       entry['response']['content']['size'] / 1024.0,
                       entry['request']['url']
                       )
                      for entry in entries]
    simple_entries.sort(key=(lambda i: i[0]), reverse=True)
    for time, size, url in simple_entries:
        print "{0} ms, {1} KB, URL {2}".format(time, size, url)

if __name__ == "__main__":
    main()
