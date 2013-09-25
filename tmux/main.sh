#!/bin/bash

SES='main.tmux'

tmux new -d -s $SES
tmux neww -t $SES:1
tmux neww -t $SES:2 'top'
tmux neww -t $SES:3 -n 'ipython' '. ~/python2/bin/activate; ipython'
tmux neww -t $SES:4 'mocp'
tmux selectw -t $SES:0

tmux -2 attach -t $SES
