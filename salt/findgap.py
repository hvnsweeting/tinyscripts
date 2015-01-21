#!/usr/bin/env python2
import argparse
import datetime
import sys

'''
by hvn@familug.org at Wed Jan 21 16:49:15 ICT 2015

Find most time-consuming tasks: (column 3 is calculated gaps between 2
consecutive steps)
$ python findgap.py develop-stdout.log -v -l 100 | sort -k1,1 -n

Expected log format:
2015-01-18 17:20:58,646 salt.loader (loader.gen_functions:846) Loaded virtualenv_mod as virtual virtualenv
'''


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('LOGFILE')
    argp.add_argument('--verbose', '-v', action='store_true')
    argp.add_argument('--larger-equal', '-l', metavar='N seconds',
                      type=int, default=20)

    args = argp.parse_args()

    prior_line = ''
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
            prior_tobj = timeobj

        # two steps which only different in milliseconds,
        # skip but save prior line. This is optimization, avoid to
        # calculate gap when it is insignificant.
        # Even it just saves 1 milliseconds for each, when input
        # is 10 million lines, that help save much time.
        if prior_tobj == timeobj:
            prior_line = line
            continue

        gap, prior_tobj = (timeobj - prior_tobj).total_seconds(), timeobj
        if gap < args.larger_equal:
            prior_line = line
            continue

        # gap position must be consistent, output must on 1 line to be able to
        # feed output to other UNIX tools - e.g sort -k1,1
        if args.verbose:
            output = '{0} seconds FROM {1} ---> {2}'
            print output.format(gap, prior_line.strip(), line.strip())
        else:
            print gap, timestr

        prior_line = line

if __name__ == "__main__":
    main()
