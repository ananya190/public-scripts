#!/bin/zsh

SESSION="battle-stations"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)
BATTLESTATIONDIR="/Users/ananyageorge/Documents/projects/battle-stations/"

if [ "$SESSIONEXISTS" = "" ]
then
tmux new-session -d -c $BATTLESTATIONDIR -stations/ -s $SESSION 

# go to battle station planning directory
tmux rename-window -t $SESSION:1 'admin'
tmux send-keys -t $SESSION:1 'cdkbbs' C-m 'clear' C-m
tmux send-keys -t $SESSION:1 'task scrum project:battlestation' C-m

# open project dir
tmux new-window -t $SESSION:2 -c $BATTLESTATIONDIR
tmux send-keys -t $SESSION:2 'lsd' C-m

/Users/ananyageorge/.scripts/scripting-tmux/enter-or-switch-session.sh $SESSION:1
else
/Users/ananyageorge/.scripts/scripting-tmux/enter-or-switch-session.sh $SESSION
fi

