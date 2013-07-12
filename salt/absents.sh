#!/bin/bash
# get all absent states
if [ -z $1 ]; then
    echo "USAGE: $0 path_to_salt_states"; exit 1
fi

cd $1
find | grep absent | grep -v '.git' | sed -e 's:/:.:g' -e 's/.sls//' -e 's/\.\.//g' | sort -n
