#!/bin/bash

#Step1: Create 

INTERFACE="upfgtp"
TUNNEL="vxlan0"

# Add the ingress qdisc at upfgtp interface
tc qdisc add dev $INTERFACE handle ffff: ingress
tc filter add dev $INTERFACE parent ffff: protocol all u32 match u32 0 0 action mirred egress mirror dev $TUNNEL


##Removign Filters and qdisk (upf1)
#tc filter del dev upfgtp ingress
#tc qdisc del dev upfgtp ingress