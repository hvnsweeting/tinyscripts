#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Benchtest to choose the best DNS resolver.
Requires ``dig`` utility.
'''

import argparse
import collections
import subprocess

OPENDNS1 = '208.67.222.222'
OPENDNS2 = '208.67.220.220'
GOOGLEDNS1 = '8.8.8.8'
GOOGLEDNS2 = '8.8.4.4'
DNS_SERVERS = [OPENDNS1, OPENDNS2, GOOGLEDNS1, GOOGLEDNS2]


def query_A_record(domain, ip=None, times=100):
    counter = collections.Counter()
    basecmd = ['dig', domain]
    for server in DNS_SERVERS:
        cmd = basecmd[:] + ['@' + server]
        print('Resolving by {0}'.format(server))
        for i in range(times):
            output = subprocess.check_output(cmd)
            if ip in output:
                counter.update([server])
    return counter


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('domain')
    argp.add_argument('ip')
    argp.add_argument('--times', '-n', default=100, type=int)
    args = argp.parse_args()
    counter = query_A_record(args.domain, args.ip, args.times)
    print("Dig {0} success rate".format(args.domain))

    for server, success in counter.iteritems():
        print('{0}: success {1} times over {2} queries, ({3}%) success'.format(
              server, success, args.times, float(success)/args.times*100))


if __name__ == "__main__":
    main()
