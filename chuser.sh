#!/bin/bash
# by Hung Nguyen Viet <hvn@familug.org>
# Sun Mar 16 23:09:05 ICT 2014

if [ $(id -u) -ne 0 ]; then
  echo "Must run as root"
  exit 1
fi

if [ $# -ne 2 ]; then
  echo "Usage $0 <username> <password>"
  exit 1
fi

useradd $1 --create-home --shell /bin/bash
echo $1:$2 | chpasswd
