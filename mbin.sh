#!/bin/bash

if [[ ! -d ~/bin ]]; then
    mkdir ~/bin
fi
set -x
for i in *.sh; do
    if [[ ! -e ~/bin/$i ]]; then
        ln -s `pwd`/$i ~/bin/$i
    fi
done
set +x
