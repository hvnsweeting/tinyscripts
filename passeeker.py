#!/usr/bin/env python2

import argparse
import os

SENSITIVE_KEYWORDS = (
    'api',
    'token',
    'pass',
    'secret',
    'private',
    'signature',
    'database',
)

PERMITTED_LENGTH = 200


def false(line):
    return False


def seek_result(filepath, skip_func=false):
    printed_filename = False
    with open(filepath) as f:
        idx = 1
        for line in f:
            line = line.lower().rstrip()
            if any(kw in line for kw in SENSITIVE_KEYWORDS):
                if skip_func(line):
                    continue
                if printed_filename is False:
                    print('Found in %s' % filepath)
                    printed_filename = True
                yield '%4d %s' % (idx, line[:PERMITTED_LENGTH])
            idx += 1


def main():
    argp = argparse.ArgumentParser(__doc__)
    argp.add_argument('files', nargs='+')
    args = argp.parse_args()

    skip_func = false
    for path in args.files:
        if os.path.isfile(path):
            for found in seek_result(path, skip_func):
                print(found)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for f in files:
                    fullpath = os.path.join(root, f)
                    for found in seek_result(fullpath, skip_func):
                        print(found)


if __name__ == "__main__":
    main()
