#!/bin/bash

echo "CMD = run suricata: Update Suricata Rules"

suricata-update

#Launcch Suricata that will use suricata yaml
suricata -c suricata.yaml -s detect-ddos.rules -i eth2

