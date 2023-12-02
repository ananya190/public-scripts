#!/bin/sh
echo "Starting tmux for checklist, go into fullscreen"
sleep 5
tmux new-session -d
tmux split-window -h
tmux split-window -p 40
tmux select-pane -t 1
tmux -2 attach-session -d
