#!/bin/zsh

SESSIONYES=$(tmux ls 2>&1 | grep -i "windows")

if [ "$SESSIONYES" = "" ]; then
  tmux
else
  if [ "$TERM_PROGRAM" != tmux ]; then
    tmux attach
  else
    tmux choose-session
  fi
fi
