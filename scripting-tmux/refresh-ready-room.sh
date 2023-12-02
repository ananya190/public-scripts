#!/bin/zsh

SESSION="ready-room"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

if [ -n "$SESSIONEXISTS" ]; then
  # open today's captain's log
  tmux kill-window -t $SESSION:3
  tmux new-window -t $SESSION:3 -n 'clog'
  tmux send-keys -t $SESSION:3 "cd /Users/ananyageorge/Dropbox/Captain\\'s\ Log/" C-m 'clog' C-m
  # tmux send-keys -t 'clog' 'clog' C-m

  # open today's field notes
  tmux kill-window -t $SESSION:4
  tmux new-window -t $SESSION:4 -n 'fnote'
  tmux send-keys -t $SESSION:4 'cd $HOME/.scripts/field-notes/' C-m 'fnote' C-m
  # tmux send-keys -t 'fnote' 'fnote' C-m
else
  ~/.scripts/scripting-tmux/build-ready-room.sh
fi

