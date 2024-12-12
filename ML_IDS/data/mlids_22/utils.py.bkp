import subprocess
import json
import requests
import ipaddress
import pandas as pd
from datetime import datetime
from config import get_enforcment_strategy, MS_IP_POOL
import os

class CoreNetworkAPI:
    @staticmethod
    def release_pdu(ip, mapping_data="mapping_data.txt", slice=2):
        cntxt = None
        with open(mapping_data, "r") as f:
            lines = f.readlines()
            for l in lines:
                cntxt, _ip, supi = l.split("\t")
                _ip = _ip.split(":")[1].strip()
                cntxt = cntxt.split(" ")[1].strip()
                if _ip == ip:
                    url = f"http://smf{slice}.free5gc.org:8000/nsmf-pdusession/v1/sm-contexts/{cntxt}/release"
                    print(url)
                    CoreNetworkAPI._send_curl_request(url, "POST")
                    break
        CoreNetworkAPI._update_mapping_file(cntxt, mapping_data)

    @staticmethod
    def change_throughput(ip, mapping_data="mapping_data.txt", slice=2, max_dl='5 Mbps', max_ul='1 Mbps', qos="20"):
        cntxt = None
        url = None
        with open(mapping_data, "r") as f:
            lines = f.readlines()
            for l in lines:
                cntxt, _ip, supi = l.split("\t")
                _ip = _ip.split(":")[1].strip()
                cntxt = cntxt.split(" ")[1].strip()
                if _ip == ip:
                    url = f"http://smf{slice}.free5gc.org:8000/nsmf-callback/sm-policies/{cntxt}/update"
                    print(url)
                    break
        
        if url:
            post_headers = {
                "accept": "application/json",
                "Content-Type": "application/json"
            }
            post_data = {
                "smPolicyDecision": {
                    "pccRules": {
                        "PccRuleId-1": {
                            "flowInfos": [
                                {
                                    "flowDescription": "permit out ip from any to assigned",
                                    "flowDirection": "DOWNLINK"
                                }
                            ],
                            "pccRuleId": "PccRuleId-1",
                            "precedence": 100,
                            "refQosData": [f"{qos}"]
                        }
                    },
                    "qosDecs": {
                        f"{qos}": {
                            "qosId": f"{qos}",
                            "5qi": 3,
                            "maxbrUl": max_ul,
                            "maxbrDl": max_dl,
                            "gbrUl": "0 Mbps",
                            "gbrDl": "0 Mbps"
                        }
                    }
                }
            }

            post_response = requests.post(url, headers=post_headers, json=post_data)
            if post_response.status_code == 200:
                print("POST request was successful.")
            else:
                print(f"Failed to send POST request. Status code: {post_response.status_code}")

    @staticmethod
    def _update_mapping_file(cntxt, mapping_data="mapping_data.txt"):
        with open(mapping_data, "r") as f:
            lines = f.readlines()
        new_lines = ""
        for l in lines:
            _cntxt, _ip, _supi = l.split("\t")
            _cntxt = _cntxt.split(" ")[1].strip()
            if cntxt == _cntxt:
                continue
            else:
                new_lines += l
        with open(mapping_data, "w") as f:
            f.write(new_lines)

    @staticmethod
    def _send_curl_request(url, method):
        try:
            result = subprocess.run(['curl', '-X', method, url], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Curl request failed: {result.stderr}")
                return None
            return result.stdout
        except subprocess.SubprocessError as e:
            print(f"An error occurred while sending the curl request: {e}")
            return None

    # Creates Mapping file that holds UE IP vs SM Context Info
    # @slice value "" means slice 1. As there is no number we put an empty string
    @staticmethod
    def create_mapping_data(mapping_data="mapping_data.txt", slices=["", 2, 3]):
        url = "http://amf.free5gc.org:8000/namf-oam/v1/registered-ue-context" 
        try:
            json_response = CoreNetworkAPI._send_curl_request(url, "GET")
            if json_response is None:
                return

            data = json.loads(json_response)
            for item in data:
                if item["PduSessions"] is None:
                    continue
                
                supi = item.get('Supi')
                sm_contexts = [k["SmContextRef"] for k in item["PduSessions"]]

                for smcntxt in sm_contexts:
                    for slice in slices:
                        sm_url = f"http://smf{slice}.free5gc.org:8000/nsmf-oam/v1/ue-pdu-session-info/{smcntxt}"
                        json_response = CoreNetworkAPI._send_curl_request(sm_url, "GET")
                        if json_response == "null" or json_response is None:
                            continue
                        else:
                            json_response = json.loads(json_response)
                            ip = json_response["PDUAddress"]
                        
                        with open(mapping_data, 'a') as file:
                            line = f"SmContext: {smcntxt}\tip: {ip}\tSupi: {supi}\n"
                            file.write(line)
        except Exception as e:
            print(f"An error occurred in create_mapping_data: {e}")


##throttle the throughput
def change_throughput(ip):
    CoreNetworkAPI.change_throughput(ip)

## Create the mapping data
def create_mapping_data(mapping_data="mapping_data.txt"):
    CoreNetworkAPI.create_mapping_data(mapping_data=mapping_data, slices=[2])

##Extract UE and Server IP:
def extract_ip_addresses_from_flow(flow):
    ue_blocks = ['10.60.0.0/24', '10.61.0.0/24', '10.62.0.0/24']

    # Extract the first two IP addresses
    ip1, ip2 = flow.split('_')[:2]

    # List of IP address blocks
    ue_blocks = MS_IP_POOL

    # Convert CIDR blocks to IPv4Network objects
    ue_networks = [ipaddress.ip_network(block) for block in ue_blocks]

    # Initialize matched and non-matched IPs
    matched_ip = None
    nonmatched_ip = None

    # Function to check if IP belongs to a CIDR block
    def check_ip(ip):
        for network in ue_networks:
            if ipaddress.ip_address(ip) in network:
                return True
        return False

    # Check the IP addresses
    for ip in [ip1, ip2]:
        if check_ip(ip):
            matched_ip = ip
        else:
            nonmatched_ip = ip

    # Output results
    print(f"Source IP:", matched_ip)
    print("Destination IP:", nonmatched_ip)
    return matched_ip, nonmatched_ip

# Monitor and process attack records
def monitor_attacks(flow_id):
    source_ip, destination_ip = extract_ip_addresses_from_flow(flow_id)
    strategy = get_enforcment_strategy(type='type_1')
    # Load CSV file
    file_name = 'attack_records.csv'
    df = initialize_attack_record(file_name=file_name)
      # Timestamp for current attack
    attack_timestamp = datetime.now()

    # Check if the source IP already has records in the file
    attack_count = df[df['source_ip'] == source_ip].shape[0]

    # Default mitigation action (None unless thresholds are hit)
    mitigation_action = ''

   
    if attack_count + 1 >= strategy['pdu_session_deletion_limit']:
        # Delete PDU session
        mitigation_action = 'PDU Session Deleted'
        #delete_pdu_session(source_ip)  # Assuming you have a function for this action
        CoreNetworkAPI.release_pdu(source_ip)

    elif attack_count + 1 in strategy['throttle_intervals']:
        # Apply throttle based on the number of attacks
        index = strategy['throttle_intervals'].index(attack_count + 1)
        #throttle_network(source_ip, strategy["throttled_by"][index])  # Throttle function
        max_dl, max_ul, qos = strategy["max_dl"][index], strategy["max_ul"][index], strategy["qos"][index]
        mitigation_action = f'max_ul: {max_ul}, max_dl: {max_dl}'
        CoreNetworkAPI.change_throughput(source_ip, mapping_data="mapping_data.txt", slice=2, max_dl=max_dl, max_ul=max_ul, qos=qos)
    
    # Create a new record for the current attack
    new_record = pd.DataFrame([{
        'source_ip': source_ip,
        'dest_ip': destination_ip,
        'flow_id': flow_id,
        'attack_timestamp': attack_timestamp,
        'mitigation_action': mitigation_action
    }])
    
    # Append the new attack to the dataframe and save to CSV
    df = pd.concat([df, new_record], ignore_index=True)
    df.to_csv(file_name, index=False)

    print(f"Attack Detected: from {source_ip} to {destination_ip}, action taken: {mitigation_action}")


# Initialize or load attack_records CSV file
def initialize_attack_record(file_name):
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        # Create CSV with headers if it doesn't exist
        df = pd.DataFrame(columns=['source_ip', 'dest_ip', 'flow_id', 'attack_timestamp', 'mitigation_action'])
        df.to_csv(file_name, index=False)
    return df


## Delete Files based on name/location
def delete_files(file_list=[]):
    for file_path in file_list:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        else:
            print(f"File does not exist: {file_path}")

