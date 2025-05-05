import subprocess
import time
from datetime import datetime

def run_command_in_container(container_name, command):
    """
    Executes a command inside a specified Docker container.
    
    Args:
        container_name (str): Name of the container.
        command (str): Command to execute inside the container.
    """
    try:
        subprocess.run(["docker", "exec", container_name] + command.split(), check=True)
        print(f"[INFO] Command '{command}' executed in container '{container_name}' at {datetime.now()}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to execute command '{command}' in container '{container_name}': {e}")


def main():
    # Define time intervals (in seconds)
    time_intervals = [5, 40]  # Replace with your actual times

    # Define container names and commands
    container_commands = {
        "ue12": {
            "time1": "iperf3 -c 10.50.50.12 -u -b 0.12M -t 500 --bidir",
        },
        "ue21": {
            "time1": "iperf3 -c 10.50.50.50 -u -b 0.1M -t 500 --bidir",
            "time2": "python3 /data/generate_attack.py",
        },
    }

    # Start executing commands at each interval
    start_time = time.time()

    # Execute commands at time1
    time.sleep(time_intervals[0])
    for container, commands in container_commands.items():
        if "time1" in commands:
            run_command_in_container(container, commands["time1"])

    # Execute commands at time2
    time.sleep(time_intervals[1] - time_intervals[0])
    for container, commands in container_commands.items():
        if "time2" in commands:
            run_command_in_container(container, commands["time2"])

    print("[INFO] All commands executed.")

if __name__ == "__main__":
    main()
