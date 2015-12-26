#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
Script for getting image ID from slug.

Author: Viet Hung Nguyen <hvn@familug.org>

Requires: python-digitalocean
'''

import argparse
import os
import sys

import digitalocean


def get_id_from_slug(manager, slug):
    for img in manager.get_distro_images():
        if img.slug == slug:
            return img.id


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('slugs', nargs='*', type=str,
                      help='slug(s) for the image'
                      )
    args = argp.parse_args()

    try:
        token = open(os.path.expanduser('~/.digitalocean')).read().strip()
    except IOError as e:
        print e
        print "Please put a DigitalOcean API v2 token to ~/.digitalocean"
        sys.exit(1)

    manager = digitalocean.Manager(token=token)
    slugs = args.slugs or ('ubuntu-14-04-x64', 'ubuntu-12-04-x64')
    for slug in slugs:
        print slug, get_id_from_slug(manager, slug)

if __name__ == "__main__":
    main()
