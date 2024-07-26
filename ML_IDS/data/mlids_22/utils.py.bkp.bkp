# reading suricata logs and creates alerts accordingly
# it will make API call through privnet bridge to the Core Functions

import subprocess
import json
import requests
from tailer import follow

def release_pdu(ip):
    cntxt = None
    with open("mapping_data.txt", "r") as f:
        lines = f.readlines()
        for l in lines:
            cntxt, _ip, supi = l.split("\t")
            _ip = _ip.split(":")[1].strip()
            cntxt = cntxt.split(" ")[1].strip()
            if _ip == ip:
                url = "http://smf2.free5gc.org:8000/nsmf-pdusession/v1/sm-contexts/"+cntxt+"/release"
                print(url)
                send_curl_request(url, "POST")
                break
    update_file(cntxt)


def change_throughput(ip, mapping_data="mapping_data.txt"):
    cntxt = None
    with open(mapping_data, "r") as f:
        lines = f.readlines()
        for l in lines:
            cntxt, _ip, supi = l.split("\t")
            _ip = _ip.split(":")[1].strip()
            cntxt = cntxt.split(" ")[1].strip()
            if _ip == ip:
                url = "http://smf2.free5gc.org:8000/nsmf-callback/sm-policies/"+cntxt+"/update"
                print(url)
    #hard coded
    # If urn:uuid is saved in "mapping data" we can make tbe below with 1 request no need for "get_url" request
    # http://amf.free5gc.org:8000/namf-oam/v1/registered-ue-context
    # get_url = "http://pcf.free5gc.org:8000/npcf-smpolicycontrol/v1/sm-policies/imsi-208930000000001-1"
    # get_headers = {
    #     "accept": "application/json"
    # }

    # Send the GET request
    # response = requests.get(get_url, headers=get_headers)
    #print(response.json()["context"]["notificationUri"])
    # Check if the request was successful
    # if response.status_code == 200:
    #     # Parse the JSON response
    #     data = response.json()["context"]
        
    #     # Extract the notificationUri element
    #     notification_uri = data.get("notificationUri")
        
    #     # Print or store the notificationUri
    #     if notification_uri:
    #         print(f"notificationUri: {notification_uri}")
        # Step 2: Send the POST request
            # Define the POST endpoint (appending /update to the notification URI)
            #post_url = f"{notification_uri}/update"
    post_headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
    post_data = {
        #"resourceUri": get_url,
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
                    "refQosData": ["10"]
                }
            },
            "qosDecs": {
                "10": {
                    "qosId": "10",
                    "5qi": 3,
                    "maxbrUl": "12 Mbps",
                    "maxbrDl": "12 Mbps",
                    "gbrUl": "0 Mbps",
                    "gbrDl": "0 Mbps"
                }
            }
        }
    }

        # Send the POST request
    post_response = requests.post(url, headers=post_headers, json=post_data)
        # Check if the POST request was successful
    if post_response.status_code == 200:
        print("POST request was successful.")
    else:
        print(f"Failed to send POST request. Status code: {post_response.status_code}")
        # else:
        #     print("notificationUri not found in the response.")
    # else:
    #     print(f"Failed to retrieve data. Status code: {response.status_code}")



def update_file(cntxt, mapping_data="mapping_data.txt"):
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
    with open("mapping_data.txt", "w") as f:
        f.write(new_lines)