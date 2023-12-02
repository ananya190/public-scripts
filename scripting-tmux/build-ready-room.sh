#!/bin/zsh

SESSION="ready-room"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

if [ "$SESSIONEXISTS" = "" ]
then
tmux new-session -d -s $SESSION

# open taskwarrior-tui
tmux rename-window -t $SESSION:1 'taskwarrior'
tmux send-keys -t $SESSION:1 'tt' C-m
# tmux send-keys -t 'taskwarrior' 'tt' C-m

# open everything-repository
tmux new-window -t $SESSION:2 -n 'wiki'
tmux send-keys -t $SESSION:2 'cdwiki' C-m 'nvim .' C-m
# tmux send-keys -t 'wiki' 'cdwiki' C-m 'nvim .' C-m

# open today's captain's log
tmux new-window -t $SESSION:3 -n 'clog'
tmux send-keys -t $SESSION:3 "cd /Users/ananyageorge/Dropbox/Captain\\'s\ Log/" C-m 'clog' C-m
# tmux send-keys -t 'clog' 'clog' C-m

# open today's field notes
tmux new-window -t $SESSION:4 -n 'fnote'
tmux send-keys -t $SESSION:4 'cd $HOME/.scripts/field-notes/' C-m 'fnote' C-m
# tmux send-keys -t 'fnote' 'fnote' C-m

# open trying-stuff-out directory
tmux new-window -t $SESSION:5
tmux send-keys -t $SESSION:5 'cd ~/Documents/trying-stuff-out' C-m 'clear' C-m
# tmux send-keys -t 'temp' 'cd ~/Documents/trying-stuff-out' C-m 'clear' C-m

# open $home directory
tmux new-window -t $SESSION:6
tmux send-keys -t $SESSION:6 'cd ~' C-m 'clear' C-m

fi
