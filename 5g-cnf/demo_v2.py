import subprocess
import time
from datetime import datetime
from threading import Thread

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

def execute_commands_in_parallel(container_commands, time_key):
    threads = []
    for container, commands in container_commands.items():
        if time_key in commands:
            thread = Thread(target=run_command_in_container, args=(container, commands[time_key]))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

def main():
    # Define time intervals (in seconds)
    time_intervals = [5, 40]  # Replace with your actual times

    # Define container names and commands
    container_commands = {
        "ue12": {
            "time1": "iperf3 -c 10.50.50.12 -u -b 0.12M -t 800 --bidir",
        },
        "ue21": {
            "time1": "iperf3 -c 10.50.50.50 -u -b 0.1M -t 800 --bidir",
            "time2": "python3 /data/generate_attack.py",
        },
    }

    # Start executing commands at each interval
    start_time = time.time()

    # Execute commands at time1
    time.sleep(time_intervals[0])
    execute_commands_in_parallel(container_commands, "time1")

    # Execute commands at time2
    time.sleep(time_intervals[1] - time_intervals[0])
    execute_commands_in_parallel(container_commands, "time2")

    print("[INFO] All commands executed.")

if __name__ == "__main__":
    main()
