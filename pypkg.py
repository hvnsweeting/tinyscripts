#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# by Hung Nguyen Viet <hvn@familug.org>
# Thu Sep  4 00:03:46 ICT 2014

import argparse
import subprocess as spr
import logging
import os

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def grep(dest=None, check_def=False, cls=True):
    if not dest:
        dest = '.'

    cls_expr = '^class' if cls else ''
    def_expr = '|def ' if check_def else ''

    old_dir = os.getcwd()
    os.chdir(dest)
    cmd_fm = "grep -Rin -E {0}{1} ."
    cmd = cmd_fm.format(cls_expr, def_expr, dest)
    log.debug(cmd)
    print spr.check_output(cmd.split())

    os.chdir(old_dir)


def count(dest=None, ftype='.py'):
    no_files = 0
    locs = 0

    def filenames():
        for d, _, fns in os.walk(dest):
            for fn in fns:
                yield os.path.join(d, fn)

    for fn in filenames():
        no_files += 1
        fd = open(fn)
        loc = sum(1 for line in fd)
        print '%5d %s' % (loc, fn)
        locs += loc
        fd.close()

    print 'Total of files:', no_files
    print 'Total of lines:', locs


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('dest', help='dest to perform evaluate code')
    argp.add_argument('--func', action='store_true',
                      help='also grep for function definition')

    args = argp.parse_args()
    grep(args.dest, args.func)
    count(args.dest)


if __name__ == "__main__":
    main()
