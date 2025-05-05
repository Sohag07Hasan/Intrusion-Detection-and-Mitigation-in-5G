#!/bin/bash

# Start iperf3 server in the background and save output to a file
iperf3 -s > iperf_server_output.txt &

# Save the background process PID to allow it to keep running
iperf_pid=$!

# Wait for 1 second
#sleep 1

# Show real-time logs
tail -f iperf_server_output.txt

# Optional: Wait for iperf3 to finish (if you want to wait for the process to end)
wait $iperf_pid
