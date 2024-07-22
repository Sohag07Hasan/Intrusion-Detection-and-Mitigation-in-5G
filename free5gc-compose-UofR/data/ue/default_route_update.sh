#!/bin/bash

# Name of the interface for the new default gateway
INTERFACE="uesimtun0"
# IP of the new default gateway
IP_ADDRESS=$(ip addr show $INTERFACE | grep 'inet ' | awk '{print $2}' | cut -f1 -d'/')

# Check if an IP address was found
if [ -z "$IP_ADDRESS" ]; then
    echo "No IP address found for interface $INTERFACE."
else
    echo "The IP address for $INTERFACE is $IP_ADDRESS"
    ip route del default
    ip route add default via $IP_ADDRESS dev $INTERFACE
fi

ip route
