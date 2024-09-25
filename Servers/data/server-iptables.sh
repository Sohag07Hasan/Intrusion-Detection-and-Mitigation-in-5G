#!/bin/bash
#
# Configure iptables in all Servers
#
# Entries for Slice 1 {upf ip: 10.200.200.10, ms_pool: 10.60.0.0/24 }
ip route add 10.60.0.0/24 via 10.200.200.10 

# Entries for Slice 2 {upf ip: 10.200.200.20, ms_pool: 10.61.0.0/24 }
ip route add 10.61.0.0/24 via 10.200.200.20 
