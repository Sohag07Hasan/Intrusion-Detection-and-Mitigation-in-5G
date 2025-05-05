
#!/bin/sh
## This is a comment!



filename=$1
time_budget=20000

# Name of the interface for the new default gateway
INTERFACE="uesimtun0"
IP_ADDRESS=$(ip addr show $INTERFACE | grep 'inet ' | awk '{print $2}' | cut -f1 -d'/')

# Check if an IP address was found
if [ -z "$IP_ADDRESS" ]; then
    echo "No IP address found for interface $INTERFACE."
else
	echo "Process Started"	
	urls=`cat $filename`
	for url in $urls; do
		google-chrome-stable --headless --disable-gpu --disable-dev-shm-usage --no-sandbox --dump-dom --virtual-time-budget=$time_budget $url
		sleep 0.5
	done

fi