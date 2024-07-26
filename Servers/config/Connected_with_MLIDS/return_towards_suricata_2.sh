#!/bin/bash
#
# This script will ensure return traffic towards UE.
# If you choose a route upf > mlids_21, ensure same back route
# for Simility I am trying to keep the name as used inside upf
# Forward Traffic: upf2 -> "mlids_21/mlids_22/Suricata_2" -> server-mlids_21
# Return/Back Traffic: server-mlids_21 > "mlids_21/mlids_22/Suricata_2" > upf2

# Suricata_2 IP is: 10.50.50.130
ip route add 10.61.0.0/24 via 10.50.50.130
