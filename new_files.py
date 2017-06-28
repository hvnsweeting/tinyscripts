#!/usr/bin/env python


__doc__ = '''
Get list of newest files in given directory
'''
import os
import time


def get_human_time(filepath):
    return time.strftime(
        '%Y-%m-%d',
        time.gmtime(int(os.stat(filepath).st_ctime))
    )


def get_newest_files(root, n):
    files = [os.path.join(root, f) for f in os.listdir(root)
             if not f.startswith('.')]
    files.sort(key=lambda f: os.stat(f).st_ctime, reverse=True)
    return files[:n]


def main():
    import argparse
    argp = argparse.ArgumentParser(__doc__)
    argp.add_argument(
        'directory', help='Where to look for files',
    )
    argp.add_argument(
        '-n', help='Number of files, default to 10',
        type=int, default=10,
    )
    args = argp.parse_args()

    root = args.directory
    files = get_newest_files(root, args.n)

    for filepath in files:
        print(
            "{0} {1}".format(get_human_time(filepath),
                             os.path.basename(filepath))
        )


if __name__ == "__main__":
    main()
