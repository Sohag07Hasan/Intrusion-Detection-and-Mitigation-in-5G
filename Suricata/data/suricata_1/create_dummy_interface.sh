#!/bin/bash

# Load dummy module and setup interface
modprobe dummy
ip link add dummy0 type dummy
ip link set dummy0 up
ip addr add 192.168.1.100/24 dev dummy0

# Run the main process (keep this as the last command)
exec "$@"
