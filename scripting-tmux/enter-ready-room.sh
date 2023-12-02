#!/bin/zsh

SESSION="ready-room"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

if [ "$SESSIONEXISTS" = "" ]
then
  ~/.scripts/scripting-tmux/build-ready-room.sh
fi

~/.scripts/scripting-tmux/enter-or-switch-session.sh $SESSION
