#!/bin/bash

FRONTEND=byobu
ACTIVE_IFACE=$(ip li | grep 'state UP' | head -n 1 | awk '{print $2}' | tr -d ':')

$FRONTEND new -d -s hvn
$FRONTEND neww -t hvn:6 -n 'mon' 'top'
$FRONTEND splitw -t hvn:6 'tail -f /var/log/syslog | ccze'
$FRONTEND neww -t hvn:7 -n 'iftop' "sudo iftop -i $ACTIVE_IFACE"
$FRONTEND selectw -t hvn:0 

$FRONTEND -2 attach -t hvn
