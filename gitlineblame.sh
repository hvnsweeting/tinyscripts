#!/bin/bash
# by Viet Hung Nguyen <hvn@familug.org>
# find the commit introduce a piece of content (one word, or a line of code).

FILE=$1
KEYWORD="$2"

echo "Looking for the commit on $FILE who introduced content: $KEYWORD"
for hash in `git log --format='%H' -- $FILE`; do
    git show $hash:$FILE | grep -q "$KEYWORD" && last=$hash
done
git log -n1 $last
