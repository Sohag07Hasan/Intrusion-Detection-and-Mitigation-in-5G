# reading suricata logs and creates alerts accordingly
# it will make API call through privnet bridge to the Core Functions

import subprocess
import json
import requests
from tailer import follow

def call_api(alert_data):
    url = "https://api.example.com/notify"  # API endpoint
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=alert_data)
    print("API Response:", response.text)

def monitor_alerts(logfile):
    threshold = 5
    count = {}
    for line in follow(open(logfile)):
        try:
            alert = json.loads(line)
            if alert.get('event_type') == 'alert' and 'DoS' in alert.get('alert', {}).get('signature', ''):
                ip = alert["flow"]["src_ip"]
                print("Alert: ", ip)
                if ip not in count.keys():
                    count[ip] = 1
                else:
                    count[ip] += 1
                    if count[ip] == threshold:
                        del count[ip]
                        print("Releasing PDU")
                        release_pdu(ip)
                
        except json.JSONDecodeError:
            continue

def send_curl_request(url, method):
    result = subprocess.run(['curl', '-X', method, url], capture_output=True, text=True)

def release_pdu(ip):
    cntxt = None
    with open("mapping_data.txt", "r") as f:
        lines = f.readlines()
        for l in lines:
            cntxt, _ip, supi = l.split("\t")
            _ip = _ip.split(":")[1].strip()
            cntxt = cntxt.split(" ")[1].strip()
            if _ip == ip:
                url = "http://smf.free5gc.org:8000/nsmf-pdusession/v1/sm-contexts/"+cntxt+"/release"
                print(url)
                send_curl_request(url, "POST")
                break
    update_file(cntxt)



def update_file(cntxt):
    with open("mapping_data.txt", "r") as f:
        lines = f.readlines()
    new_lines = ""
    for l in lines:
        _cntxt, _ip, _supi = l.split("\t")
        _cntxt = _cntxt.split(" ")[1].strip()
        if cntxt == _cntxt:
            continue
        else:
            new_lines += l
    with open("mapping_data.txt", "w") as f:
        f.write(new_lines)


if __name__ == "__main__":
    log_file = '/var/log/suricata/eve.json'  # Adjust to your log file location
    monitor_alerts(log_file)
