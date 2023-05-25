#!/bin/sh
tmux split-window -v -p 25
tmux split-window -h -p 30
tmux select-pane -t 1
tmux split-window -h -p 30
tmux select-pane -t 1 
nvim .
