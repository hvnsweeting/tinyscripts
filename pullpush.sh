#!/bin/bash

if [[ -z $1 ]];then
    CMD='pull'
else
    CMD=$1
fi

cd ..
for dir in *;do
    cd $dir
    pwd
    git $CMD origin master
    cd ..
done

