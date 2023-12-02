#!/bin/zsh

SESSION="script-room"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

if [ "$SESSIONEXISTS" = "" ]
then
  cd ~/.scripts/
  tmux new-session -d -s $SESSION
  tmux send-keys -t $SESSION:1 'nvim .' C-m
  tmux new-window -t $SESSION:2
  tmux send-keys -t $SESSION:2 'cd ~/.config' C-m 'clear' C-m
fi

~/.scripts/scripting-tmux/enter-or-switch-session.sh $SESSION:1
