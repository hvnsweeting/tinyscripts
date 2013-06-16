#!/bin/bash

FRONTEND=tmux
SESSION=mail

$FRONTEND new -d -s $SESSION
$FRONTEND neww -t $SESSION:1 -n 'hvnsweeting' "mutt -F ~/mails/hvnsweeting"
$FRONTEND -2 attach -t $SESSION
