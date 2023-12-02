#!/bin/zsh

SESSION="deep-learning"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

if [ "$SESSIONEXISTS" = "" ]; then
tmux new-session -d -s $SESSION
tmux send-keys -t $SESSION:1 'cddl' C-m 'clear' C-m
fi

~/.scripts/scripting-tmux/enter-or-switch-session.sh $SESSION
