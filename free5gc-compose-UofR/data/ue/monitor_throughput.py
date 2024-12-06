import time

# Specify the interface you want to monitor
network_interface = "uesimtun0"  # Change this to the desired interface (e.g., eth1, wlan0)

# File to read network statistics
proc_net_dev_path = "/proc/net/dev"

def get_network_stats(interface):
    """
    Reads /proc/net/dev and retrieves RX and TX bytes for a given network interface.
    """
    try:
        with open(proc_net_dev_path, "r") as f:
            lines = f.readlines()
        for line in lines:
            if interface in line:
                data = line.split()
                rx_bytes = int(data[1])  # Bytes received
                tx_bytes = int(data[9])  # Bytes transmitted
                return rx_bytes, tx_bytes
    except FileNotFoundError:
        print(f"Error: {proc_net_dev_path} not found!")
    except Exception as e:
        print(f"Error reading network stats for {interface}: {e}")
    return 0, 0

# Initialize previous stats
previous_rx, previous_tx = get_network_stats(network_interface)
previous_time = time.time()

print(f"Monitoring throughput on interface: {network_interface}")
print("Press Ctrl+C to stop.")
print(f"{'Time':<10}{'RX Throughput (Mbps)':<20}{'TX Throughput (Mbps)':<20}")

try:
    while True:
        # Wait for a short interval
        time.sleep(0.1)  # 100ms interval for real-time updates

        # Get current stats
        current_rx, current_tx = get_network_stats(network_interface)
        current_time = time.time()

        # Calculate time delta
        elapsed_time = current_time - previous_time
        if elapsed_time == 0:
            continue

        # Calculate throughput in Mbps
        rx_throughput = (current_rx - previous_rx) * 8 / (1e6 * elapsed_time)  # Mbps
        tx_throughput = (current_tx - previous_tx) * 8 / (1e6 * elapsed_time)  # Mbps

        # Print the results
        print(f"{time.strftime('%H:%M:%S'):<10}{rx_throughput:<20.2f}{tx_throughput:<20.2f}")

        # Update previous stats
        previous_rx, previous_tx = current_rx, current_tx
        previous_time = current_time

except KeyboardInterrupt:
    print("\nStopped monitoring.")
