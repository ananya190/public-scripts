#!/bin/sh
tmux new-session -d 
tmux split-window -v 
tmux split-window -h 'btm'
tmux select-pane -t 1
tmux split-window -h
tmux -2 attach-session -d
