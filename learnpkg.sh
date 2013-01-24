#!/bin/bash

# run: ./learnpkg.sh ip
pkg=$(dpkg -S $(which $1) | cut -d':' -f1 )
dpkg -s $pkg
dpkg -L $pkg
