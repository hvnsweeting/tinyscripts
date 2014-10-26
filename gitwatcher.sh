#!/bin/bash
# A script for watch upstream changes of specified files
# this needs a dedicated repo to functional properly.
# Don't use it with repo you work on, because it uses
# ``git reset --hard``
# by Hung Nguyen Viet <hvn@familug.org>
# at Sun Oct 26 10:38:29 ICT 2014
# Example: ./watcher.sh salt --branch develop doc/topics/releases/index.rst

args=$@
repodir=$1
shift

branch='master'
if [ '--branch' = $1 ]
then
    branch=$2
    shift
    shift
fi

files=$@

datafile=~/.gitwatcher
cwd=$(pwd)

cd $repodir
git fetch origin $branch 2> /dev/null
echo "Checked $args at $(date), local at $(git rev-parse HEAD)" >> $datafile

changes=$(git show ..origin/$branch -- $files)
if [ ! -z "$changes" ]; then
    echo -e "$changes" >> $datafile
    echo -e "$changes" | mail -s "New changes in $repodir" $(id -nu)
    git reset --hard origin/$branch > /dev/null
fi

function cdback {
    cd $cwd
}
trap cdback EXIT
