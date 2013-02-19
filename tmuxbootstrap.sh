#!/bin/bash

FRONTEND=tmux # this can be changed to byobu - a frontend of tmux
ACTIVE_IFACE=$(ip li | grep 'state UP' | head -n 1 | awk '{print $2}' | tr -d ':')

$FRONTEND new -d -s hvn
$FRONTEND neww -t hvn:1 -n 'mon' 'top'
$FRONTEND splitw -t hvn:1 'tail -f /var/log/syslog | ccze'
$FRONTEND neww -t hvn:2 -n 'iftop' "sudo iftop -i $ACTIVE_IFACE"
$FRONTEND selectw -t hvn:0 

$FRONTEND -2 attach -t hvn
