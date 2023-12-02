#!/bin/sh

# check if ready-room has been created

READYROOMREADY=$(tmux ls | grep "ready-room")

# if not, create it.

if [[ -z $READYROOMREADY ]]; then
  ~/.scripts/scripting-tmux/build-ready-room.sh
fi
