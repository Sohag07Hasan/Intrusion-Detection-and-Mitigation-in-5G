#!/bin/bash

# upfgtp interface is being mirrrored to suricata_1
# both IP have been made static
# upf1 ip: 10.10.10.10, #suricata ip: 10.10.10.100

# Define variables for local and remote IP addresses
LOCAL_IP="10.10.10.100"
REMOTE_IP="10.10.10.10"
LOCAL_INTERFACE="eth1"

# Define the VXLAN interface name and other parameters
VXLAN_IF="vxlan0"
VXLAN_ID="100"
VXLAN_PORT="4789"

# Check if the interface already exists
if ip link show $VXLAN_IF &> /dev/null; then
    echo "Interface $VXLAN_IF already exists, deleting it..."
    ip link del $VXLAN_IF
fi

# Create the VXLAN interface
echo "Creating VXLAN interface $VXLAN_IF..."
ip link add $VXLAN_IF type vxlan id $VXLAN_ID local $LOCAL_IP remote $REMOTE_IP dev $LOCAL_INTERFACE dstport $VXLAN_PORT

# Set the VXLAN interface up
echo "Bringing up interface $VXLAN_IF..."
ip link set $VXLAN_IF up

# Output the configuration
echo "VXLAN interface $VXLAN_IF configured with:"
echo "  Local IP: $LOCAL_IP"
echo "  Remote IP: $REMOTE_IP"
echo "  VXLAN ID: $VXLAN_ID"
echo "  VXLAN Port: $VXLAN_PORT"
