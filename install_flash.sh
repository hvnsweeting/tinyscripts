#!/bin/bash

#giai nen file tar.gz
set -x
tar xzvf $1
sudo cp -r usr/* /usr
mkdir -p ~/.mozilla/plugins
cp libflashplayer.so ~/.mozilla/plugins/
set +x
