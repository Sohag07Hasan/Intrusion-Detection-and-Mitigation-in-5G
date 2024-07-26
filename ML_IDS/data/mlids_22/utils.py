import subprocess
import json
import requests

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
    def change_throughput(ip, mapping_data="mapping_data.txt", slice=2):
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
    def create_mapping_data(mapping_data="mapping_data.txt", slices=["", 2]):
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

