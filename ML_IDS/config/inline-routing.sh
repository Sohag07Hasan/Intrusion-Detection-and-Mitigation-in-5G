#!/bin/bash

# Enable IP forwarding in the firewall container
echo 1 > /proc/sys/net/ipv4/ip_forward

# Check if iptables is installed, if not install it
if ! command -v iptables &> /dev/null
then
    echo "iptables not found, installing..."
    apt-get update
    apt-get install -y iptables
fi


# Set up IP tables in the firewall container
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT



#Adding back route towards the UE
# Entries for Slice 1 {upf ip: 10.200.200.10, ms_pool: 10.60.0.0/24 }
ip route add 10.60.0.0/24 via 10.10.10.10 

# Entries for Slice 2 {upf ip: 10.200.200.20, ms_pool: 10.61.0.0/24 }
ip route add 10.61.0.0/24 via 10.10.10.20 

#Show the IP route
ip route