import subprocess

# Function to capture real-time iPerf output and write to a file
def run_iperf_and_log(command, log_file):
    with open(log_file, 'w') as f:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
        for line in iter(process.stdout.readline, ''):
            print(line, end='')  # Print to console immediately
            f.write(line)  # Write to file without delay
        process.stdout.close()
        process.wait()

# Example command for server or client
iperf_server_command = ["iperf3", "-s"]
iperf_client_command = ["iperf3", "-c", "10.200.200.22", "--bidir", "-u", "-b", "10M"]

# Run the iPerf command with real-time logging
#run_iperf_and_log(iperf_server_command, "iperf_server_output.txt")

# To run the client-side, replace the command and run the same function
run_iperf_and_log(iperf_client_command, "iperf_client_output.txt")
