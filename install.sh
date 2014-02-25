#!/bin/bash
# This script should only run on this source dir, not its symlink

source_dir=$(pwd)
if [ -L ~/hbin ]; then
    cd ~/hbin
    if [ ! "$(pwd -P)" = "$source_dir" ]; then
        echo "~/hbin existed, remove that directory and rerun"
    fi
    cd $source_dir
else
    ln -s $(pwd) ~/hbin
    echo "export PATH=$PATH:~/hbin/" >> ~/.bashrc
fi
