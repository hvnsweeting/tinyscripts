#!/bin/bash
# a script for generating diamond processresources
# Viet Hung Nguyen <hvn@familug.org>

set -x
PID=$1
set +x
echo "exe = $(readlink /proc/$PID/exe | sed 's:\/:\\/:g')"
echo "cmdline = $(cat /proc/$PID/cmdline | sed -e 's:\/:\\/:g')"
echo "name = $(cut -d ' ' -f2 /proc/$PID/stat | tr -d \( | tr -d \) | sed -e 's:\/:\\/:g')"
