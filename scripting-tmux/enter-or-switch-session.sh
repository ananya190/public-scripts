#!/bin/zsh
#
SESSION=$1

if [ "$TERM_PROGRAM" != tmux ]; then
  tmux attach -t $SESSION
else
  tmux switch -t $SESSION
fi
