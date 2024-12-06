#!/bin/bash

output_file="container_interface_mapping.csv"

# Initialize the output file with a header
echo "Container Name,Container Interface,Host Interface" > $output_file

# Get all running container IDs
docker ps -q | while read container_id; do
    # Get the container name
    container_name=$(docker inspect --format '{{ .Name }}' "$container_id" | sed 's|/||')

    # Get the PID of the container
    pid=$(docker inspect --format '{{ .State.Pid }}' "$container_id")

    # Verify if PID was retrieved
    if [[ -z "$pid" ]]; then
        echo "Warning: Could not retrieve PID for container $container_name"
        continue
    fi

    echo "Inspecting container: $container_name (PID: $pid)"

    # Get all network interfaces inside the container
    nsenter_output=$(nsenter -t "$pid" -n ip link)
    if [[ $? -ne 0 ]]; then
        echo "Error: Unable to access network namespace for container $container_name"
        continue
    fi

    # Process each interface inside the container
    echo "$nsenter_output" | while read line; do
        if [[ "$line" == *"@"* ]]; then
            # Extract container interface and peer index
            container_interface=$(echo "$line" | awk -F': ' '{print $2}' | awk '{print $1}')
            peer_index=$(echo "$line" | grep -o '@if[0-9]*' | grep -o '[0-9]*')

            # Debugging information
            echo "Container Interface: $container_interface, Peer Index: $peer_index"

            if [[ ! -z "$peer_index" ]]; then
                # Find the corresponding host interface using peer index
                host_interface=$(ip link | grep "@if$peer_index" | awk -F': ' '{print $2}' | awk '{print $1}')

                if [[ ! -z "$host_interface" ]]; then
                    echo "Host Interface: $host_interface"
                    # Append the mapping to the CSV file
                    echo "$container_name,$container_interface,$host_interface" >> $output_file
                else
                    echo "Warning: No host interface found for container interface $container_interface"
                fi
            else
                echo "Warning: No peer index found for container interface $container_interface"
            fi
        fi
    done
done

echo "Mapping saved to $output_file"
