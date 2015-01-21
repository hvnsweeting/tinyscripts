#!/usr/bin/env python2
import argparse
import datetime
import sys

'''
by hvn@familug.org at Wed Jan 21 16:49:15 ICT 2015

Find most time-consuming tasks: (column 3 is calculated gaps between 2
consecutive steps)
$ python findgap.py develop-stdout.log -v -l 100 | sort -k3,3 -n

Expected log format:
2015-01-18 17:20:58,646 salt.loader (loader.gen_functions:846) Loaded virtualenv_mod as virtual virtualenv
'''


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('--verbose', '-v', action='store_true')
    argp.add_argument('LOGFILE')
    argp.add_argument('--larger-equal', '-l', metavar='N seconds',
                      type=int, default=0)

    args = argp.parse_args()

    SEP = 'FROM'
    SEPTO = '---->'
    last = 0
    lastline = ''
    if args.LOGFILE:
        infile = open(args.LOGFILE)
    else:
        infile = sys.stdin

    for i, line in enumerate(infile):
        try:
            timestr = line.split(',')[0]
            timeobj = datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
        except Exception:
            continue

        if i == 0:
            last = timeobj

        # two steps which only different in milliseconds,
        # skip but save last line
        if last == timeobj:
            lastline = line
            continue

        gap, last = (timeobj - last).total_seconds(), timeobj
        if gap < args.larger_equal:
            lastline = line
            continue

        if args.verbose:
            print timestr, gap, 'seconds', SEP, lastline.strip(), \
                SEPTO, line.strip()

        else:
            print timestr, gap

        lastline = line

if __name__ == "__main__":
    main()
