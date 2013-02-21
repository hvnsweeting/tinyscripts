#!/bin/bash

if [[ ! -d ~/bin ]]; then
    mkdir ~/bin
fi

for i in *.sh; do
    if [[ ! -e ~/bin/$i ]]; then
        ln -s `pwd`/$i ~/bin/$i
    fi
done
