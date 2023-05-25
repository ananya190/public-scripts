NUM=$1
task=$( sed "${NUM}q;d" ~/Documents/org/planning/todo/todo.txt )
re='(.*)status:wait(.*)'
if [[ $task =~ $re ]]; then
  task="${BASH_REMATCH[1]}status:next${BASH_REMATCH[2]}"
fi
todo.sh replace $NUM $task
