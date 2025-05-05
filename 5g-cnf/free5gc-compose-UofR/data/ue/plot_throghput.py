import time
import matplotlib.pyplot as plt
from collections import deque

# Specify the interface to monitor
network_interface = "uesimtun0"  # Change this as needed

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

# Real-time data storage
rx_throughput_data = deque(maxlen=100)
tx_throughput_data = deque(maxlen=100)
timestamps = deque(maxlen=100)

# Setup the plot
plt.ion()
fig, ax = plt.subplots()
rx_line, = ax.plot([], [], label="RX Throughput (Mbps)", color="blue")
tx_line, = ax.plot([], [], label="TX Throughput (Mbps)", color="red")
ax.set_ylim(0, 100)  # Adjust based on expected throughput
ax.set_xlim(0, 100)  # Show the last 100 points
ax.set_xlabel("Time (s)")
ax.set_ylabel("Throughput (Mbps)")
ax.legend()
ax.grid()

print(f"Monitoring real-time throughput on interface: {network_interface}")
print("Press Ctrl+C to stop.")

try:
    while True:
        # Sleep for a short interval
        time.sleep(0.1)  # Update every 100ms

        # Get current stats
        current_rx, current_tx = get_network_stats(network_interface)
        current_time = time.time()

        # Calculate elapsed time
        elapsed_time = current_time - previous_time
        if elapsed_time == 0:
            continue

        # Calculate throughput in Mbps
        rx_throughput = (current_rx - previous_rx) * 8 / (1e6 * elapsed_time)  # Mbps
        tx_throughput = (current_tx - previous_tx) * 8 / (1e6 * elapsed_time)  # Mbps

        # Update previous stats
        previous_rx, previous_tx = current_rx, current_tx
        previous_time = current_time

        #print(f"RX Throughput: {rx_throughput:.2f} Mbps, TX Throughput: {tx_throughput:.2f} Mbps")

        # Update real-time data
        rx_throughput_data.append(rx_throughput)
        tx_throughput_data.append(tx_throughput)
        timestamps.append(len(timestamps))

        # Update the plot
        rx_line.set_data(timestamps, rx_throughput_data)
        tx_line.set_data(timestamps, tx_throughput_data)
        ax.set_xlim(max(0, len(timestamps) - 100), len(timestamps))  # Keep the last 100 points
        ax.relim()
        ax.autoscale_view(True, True, False)  # Autoscale only y-axis
        plt.pause(0.01)  # Refresh the plot

except KeyboardInterrupt:
    print("\nStopped monitoring.")
    plt.ioff()
    plt.savefig("throughput_plot.png")
    #plt.show()
