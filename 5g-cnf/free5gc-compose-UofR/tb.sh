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
    echo "Executing ./free5gc-compose-UofR/docker-compose.yaml up..."
    docker compose -f ./free5gc-compose-UofR/docker-compose-core.yaml up -d > /dev/null 2>&1
    ;;
  "core down")
    echo "Executing ./free5gc-compose-UofR/docker-compose.yaml down..."
    #docker compose -f ./free5gc-compose-UofR/docker-compose-core.yaml down
    ;;
  "ran up")
    echo "Executing ./free5gc-compose-UofR/docker-compose.yaml up..."
    docker compose -f ./free5gc-compose-UofR/docker-compose-ran.yaml up -d > /dev/null 2>&1
    ;;
  "ran down")
    echo "Executing ./free5gc-compose-UofR/docker-compose.yaml down..."
    #docker compose -f ./free5gc-compose-UofR/docker-compose-ran.yaml down
    ;;
  "ue up")
    echo "Executing ./free5gc-compose-UofR/docker-compose-ue.yaml up..."
    docker compose -f ./free5gc-compose-UofR/docker-compose-ue.yaml up -d > /dev/null 2>&1
    ;;
  "ue down")
    echo "Executing ./free5gc-compose-UofR/docker-compose.yaml down..."
    #docker compose -f ./free5gc-compose-UofR/docker-compose-ue.yaml down
    ;;
  "core start")
    echo "Executing ./free5gc-compose-UofR/docker-compose.yaml up..."
    docker compose -f ./free5gc-compose-UofR/docker-compose-core.yaml start
    ;;
  "core stop")
    echo "Executing ./free5gc-compose-UofR/docker-compose.yaml down..."
    docker compose -f ./free5gc-compose-UofR/docker-compose-core.yaml stop
    ;;
  "ran start")
    echo "Executing ./free5gc-compose-UofR/docker-compose.yaml up..."
    docker compose -f ./free5gc-compose-UofR/docker-compose-ran.yaml start
    ;;
  "ran stop")
    echo "Executing ./free5gc-compose-UofR/docker-compose.yaml down..."
    docker compose -f ./free5gc-compose-UofR/docker-compose-ran.yaml stop
    ;;
  "ue start")
    echo "Executing ./free5gc-compose-UofR/docker-compose.yaml up..."
    docker compose -f ./free5gc-compose-UofR/docker-compose-ue.yaml start
    ;;
  "ue stop")
    echo "Executing ./free5gc-compose-UofR/docker-compose.yaml down..."
    docker compose -f ./free5gc-compose-UofR/docker-compose-ue.yaml stop
    ;;
  "cn list")
    echo "Executing docker ps -a --format table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.RunningFor}}"
    docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.RunningFor}}"
    ;;
  "core logs")
    echo "Executing docker compose -f ./free5gc-compose-UofR/docker-compose-core.yaml logs --follow"
    docker compose -f ./free5gc-compose-UofR/docker-compose-core.yaml logs --follow
    ;;
  "ran logs")
    echo "Executing docker compose -f ./free5gc-compose-UofR/docker-compose-core.yaml logs --follow"
    docker compose -f ./free5gc-compose-UofR/docker-compose-ran.yaml logs --follow
    ;;
  "ue logs")
    echo "Executing docker compose -f ./free5gc-compose-UofR/docker-compose-ue.yaml logs --follow"
    docker compose -f ./free5gc-compose-UofR/docker-compose-ue.yaml logs --follow
    ;;

  "server up")
    echo "Executing ./Servers/docker-compose-server.yaml up.."
    docker compose -f ./Servers/docker-compose-server.yaml up -d > /dev/null 2>&1
    ;;
  "server down")
    echo "Executing ./Servers/docker-compose-server.yaml down..."
    #docker compose -f ./Servers/docker-compose-server.yaml down
    ;;
  "server start")
    echo "Executing ./Servers/docker-compose-server.yaml start..."
    docker compose -f ./Servers/docker-compose-server.yaml start
    ;;
  "server stop")
    echo "Executing ./Servers/docker-compose-server.yaml stop..."
    docker compose -f ./Servers/docker-compose-server.yaml stop
    ;;
  "server logs")
    echo "Executing docker compose -f ./Servers/docker-compose-server.yaml logs --follow"
    docker compose -f ./Servers/docker-compose-server.yaml logs --follow
    ;;
  "mon up")
    echo "Executing ./Container-Monitoring/Container-Monitoring-Compose.yaml up.."
    docker compose -f ./Container-Monitoring/Container-Monitoring-Compose.yaml up -d > /dev/null 2>&1
    ;;
  "mon down")
    echo "Executing ./Container-Monitoring/Container-Monitoring-Compose.yaml down.."
    #docker compose -f ./Container-Monitoring/Container-Monitoring-Compose.yaml down
    ;;
  "mon start")
    echo "Executing ./Container-Monitoring/Container-Monitoring-Compose.yaml start.."
    docker compose -f ./Container-Monitoring/Container-Monitoring-Compose.yaml start
    ;;
  "mon stop")
    echo "Executing ./Container-Monitoring/Container-Monitoring-Compose.yaml stop.."
    docker compose -f ./Container-Monitoring/Container-Monitoring-Compose.yaml stop
    ;;
  "mon logs")
    echo "Executing ./Container-Monitoring/Container-Monitoring-Compose.yaml logs follow.."
    docker compose -f ./Container-Monitoring/Container-Monitoring-Compose.yaml logs --follow
    ;;
  "suricata up")
    echo "Executing ./Suricata/docker-compose-suricata.yaml up"
    docker compose -f ./Suricata/docker-compose-suricata.yaml up -d > /dev/null 2>&1
    ;;
  "suricata down")
    echo "Executing ./Suricata/docker-compose-suricata.yaml down"
    #docker compose -f ./Suricata/docker-compose-suricata.yaml down
    ;;
  "suricata start")
    echo "Executing ./Suricata/docker-compose-suricata.yaml start"
    docker compose -f ./Suricata/docker-compose-suricata.yaml start
    ;;
  "suricata logs")
    echo "Executing ./Suricata/docker-compose-suricata.yaml logs"
    docker compose -f ./Suricata/docker-compose-suricata.yaml logs --follow
    ;;
  "mlids up")
    echo "Executing ./ML_IDS/docker-compose-ml-ids.yaml up"
    docker compose -f ./ML_IDS/docker-compose-ml-ids.yaml up -d > /dev/null 2>&1
    ;;
  "mlids down")
    echo "Executing ./ML_IDS/docker-compose-ml-ids.yaml down"
    #docker compose -f ./ML_IDS/docker-compose-ml-ids.yaml down
    ;;
  "mlids start")
    echo "Executing ./ML_IDS/docker-compose-ml-ids.yaml start"
    docker compose -f ./ML_IDS/docker-compose-ml-ids.yaml start
    ;;
  "mlids stop")
    echo "Executing ./ML_IDS/docker-compose-ml-ids.yaml stop"
    docker compose -f ./ML_IDS/docker-compose-ml-ids.yaml stop
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
        tmux send-keys -t ${pane_id} "sh /data/default_route_update.sh" C-m
        tmux send-keys -t ${pane_id} "ping -c 3 8.8.8.8" C-m
        tmux send-keys -t ${pane_id} "ip route" C-m
      done
    done
    ;;    
  *)
    echo "Command not recognized."
    ;;
esac