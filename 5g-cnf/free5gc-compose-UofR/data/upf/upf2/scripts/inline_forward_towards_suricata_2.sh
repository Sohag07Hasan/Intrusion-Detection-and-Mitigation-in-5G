#!/bin/bash

#delete the default IP Route
ip route delete default

#Adding default route towards mldis21
#ip route add default via 10.10.10.222

#Adding default route towards mldis22
#ip route add default via 10.10.10.223

## Routing Towards Suricata 2
ip route add default via 10.10.10.200

#printing the ip tabel
ip route