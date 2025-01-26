#!/bin/bash

#prometheus and grafana
ssh -L 9090:localhost:9090 \
	-L 3005:localhost:3005 \
	-N -f mhr993@142.3.141.39