#!/bin/bash

# Check if we are inside a tmux session
if [ -z "$TMUX" ]; then
  echo "This script should be run from within a tmux session."
  exit 1
fi

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
  echo "No command provided."
  echo "Usage: $0 <command>"
  exit 1
fi

input_command="$1"

case $input_command in
  "core up")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-core.yaml up
    ;;
  "core down")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-core.yaml down
    ;;
  "ran up")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-ran.yaml up
    ;;
  "ran down")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-ran.yaml down
    ;;
  "ue up")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-ue.yaml up
    ;;
  "ue down")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-ue.yaml down
    ;;
  "core start")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-core.yaml start
    ;;
  "core stop")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-core.yaml stop
    ;;
  "ran start")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-ran.yaml start
    ;;
  "ran stop")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-ran.yaml stop
    ;;
  "ue start")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-ue.yaml start
    ;;
  "ue stop")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-ue.yaml stop
    ;;
  "cn list")
    echo "Executing docker ps -a --format table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.RunningFor}}"
    docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.RunningFor}}"
    ;;
  "core logs")
    echo "Executing docker compose -f docker-compose-core.yaml logs --follow"
    docker compose -f docker-compose-core.yaml logs --follow
    ;;
  "ran logs")
    echo "Executing docker compose -f docker-compose-core.yaml logs --follow"
    docker compose -f docker-compose-ran.yaml logs --follow
    ;;
  "ue logs")
    echo "Executing docker compose -f docker-compose-core.yaml logs --follow"
    docker compose -f docker-compose-ue.yaml logs --follow
    ;;
  "ue1 test")
    # Split the window into two horizontal panes
    tmux split-window -v
    # tcpdump launching at UPF
    tmux select-pane -t 0    
    tmux send-keys 'docker exec -it upf bash' C-m
    tmux send-keys 'apt -y install tcpdump' C-m
    tmux send-keys 'tcpdump' C-m
    # sednign ping command from ue
    tmux select-pane -t 1
    tmux send-keys 'docker exec -it ue1 bash' C-m
    tmux send-keys 'ping -c 10 -I uesimtun0 google.com' C-m
    ;;
  "ue5 test")
    # Split the window into two horizontal panes
    tmux split-window -v
    # tcpdump launching at UPF
    tmux select-pane -t 0    
    tmux send-keys 'docker exec -it upf2 bash' C-m
    tmux send-keys 'apt -y install tcpdump' C-m
    tmux send-keys 'tcpdump' C-m
    # sednign ping command from ue
    tmux select-pane -t 1
    tmux send-keys 'docker exec -it ue5 bash' C-m
    tmux send-keys 'ping -c 10 -I uesimtun0 google.com' C-m
    ;;
  "slice test")
    for slice_num in 1 2; do
      #Create a new Tmux window (tab) for each slice
      tmux new-window -n "Slice${slice_num}"

      #split the new window into 4 equal panes
      tmux split-window -h
      tmux select-pane -t 0
      tmux split-window -v
      tmux select-pane -t 2
      tmux split-window -v

      # Now, loop through each pane to execute commands
      for pane_id in {0..3}; do
        ue_num=$((pane_id + 1))
        # Customize your command below instead of echo
        tmux send-keys -t ${pane_id} "docker exec -it ue${slice_num}${ue_num} bash" C-m
        tmux send-keys -t ${pane_id} "ping -c 5 -I uesimtun0 8.8.8.8" C-m
      done
    done
    ;;    
  *)
    echo "Command not recognized."
    ;;
esac