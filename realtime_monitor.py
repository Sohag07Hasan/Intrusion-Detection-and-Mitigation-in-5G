import time
import requests
import matplotlib.pyplot as plt
from collections import deque

# cAdvisor configuration
CADVISOR_URL = "http://localhost:8080/metrics"  # Replace with the cAdvisor URL
CONTAINER_NAME = "ue21"  # Replace with your container name or ID
INTERFACE = "veth875c093@if37887"  # Replace with your network interface name

# Initialize deque for real-time plotting
rx_throughput_data = deque(maxlen=100)
tx_throughput_data = deque(maxlen=100)
timestamps = deque(maxlen=100)

# Setup real-time plot
plt.ion()
fig, ax = plt.subplots()
rx_line, = ax.plot([], [], label="RX Throughput (Mbps)", color="blue")
tx_line, = ax.plot([], [], label="TX Throughput (Mbps)", color="red")
ax.set_xlim(0, 100)  # Show the last 100 points
ax.set_xlabel("Time (s)")
ax.set_ylabel("Throughput (Mbps)")
ax.legend()
ax.grid()

# Function to query cAdvisor metrics
def get_cadvisor_metrics():
    try:
        response = requests.get(CADVISOR_URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cAdvisor metrics: {e}")
        return None

# Function to parse network metrics from cAdvisor output
def parse_network_metrics(metrics_text):
    rx_bytes, tx_bytes = 0, 0
    lines = metrics_text.splitlines()
    for line in lines:
        if f'container="{CONTAINER_NAME}"' in line and f'interface="{INTERFACE}"' in line:
            if "container_network_receive_bytes_total" in line:
                rx_bytes = float(line.split()[-1])
            elif "container_network_transmit_bytes_total" in line:
                tx_bytes = float(line.split()[-1])
    return rx_bytes, tx_bytes

print("Monitoring real-time throughput...")
print("Press Ctrl+C to stop.")

try:
    # Initialize previous stats
    previous_rx, previous_tx = 0, 0
    previous_time = time.time()

    while True:
        # Query cAdvisor metrics
        metrics = get_cadvisor_metrics()
        if not metrics:
            continue

        # Parse RX and TX bytes
        current_rx, current_tx = parse_network_metrics(metrics)
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

        # Update real-time data
        rx_throughput_data.append(rx_throughput)
        tx_throughput_data.append(tx_throughput)
        timestamps.append(len(timestamps))

        # Update the plot
        rx_line.set_data(timestamps, rx_throughput_data)
        tx_line.set_data(timestamps, tx_throughput_data)
        ax.set_xlim(max(0, len(timestamps) - 100), len(timestamps))  # Keep the last 100 points
        ax.set_ylim(0, max(max(rx_throughput_data, default=1), max(tx_throughput_data, default=1)) + 10)
        plt.draw()
        plt.pause(0.01)  # Refresh the plot

except KeyboardInterrupt:
    print("\nStopped monitoring.")
    plt.ioff()
    plt.show()
