#!/bin/bash

SES='tmuxws'

tmux new -d -s $SES
tmux neww -t $SES:1 -n 'rbi'
tmux neww -t $SES:2
tmux neww -t $SES:3 -n 'ipython' '. ~/python2/bin/activate; ipython'
tmux neww -n 'mrmime' -t $SES:4 'python /Users/hvn/Github/mrmime/mrmime/__init__.py'

tmux selectw -t $SES:1
tmux -2 attach -t $SES
