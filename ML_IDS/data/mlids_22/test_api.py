import requests
import json

def get_SmPolicy_by_id(sm_policy_id='imsi-208930000000005-1'):
    pcf_url = f"http://pcf.free5gc.org:8000/npcf-smpolicycontrol/v1/sm-policies/{sm_policy_id}"
    # Send a GET request to PCF to retrieve the SM Policy details
    response = requests.get(pcf_url)

    # Check if the request was successful
    # Check if the request was successful
    if response.status_code == 200:
        sm_policy_data = response.json()
        #print(f"SM Policy Data: {sm_policy_data}")
        return True, sm_policy_data
    else:
        #print(f"Failed to retrieve SM Policy. Status code: {response.status_code}")
        #print(f"Response: {response.text}")
        return False, response.text


def update_SmPolicy_by_id(sm_policy_id='imsi-208930000000005-1', sm_policy_data=''):
    pcf_update_url = f"http://pcf.free5gc.org:8000/npcf-smpolicycontrol/v1/sm-policies/{sm_policy_id}/update"
    
    # Send the updated SM Policy back to the PCF
    post_headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }


    response = requests.post(pcf_update_url, headers=post_headers, json=sm_policy_data)
    print(response)

if __name__ == "__main__":
    sm_policy_id = 'imsi-208930000000007-1'

    status, sm_policy_data = get_SmPolicy_by_id(sm_policy_id)

    if(status):
        
        # # Write JSON data to a file
        # with open('./smpolicy.json', 'w') as json_file:
        #     json.dump(sm_policy_data, json_file, indent=4)


        # Assuming sm_policy_data contains the current policy data
        
        # sm_policy_data['policy']['qosDecs'] = {
        #         "2": {
        #             "qosId": "2",
        #             "5qi": 3,
        #             "maxbrUl": "100 Mbps",
        #             "maxbrDl": "100 Mbps",
        #             "gbrUl": "0 Mbps",
        #             "gbrDl": "0 Mbps"
        #         }
        #     }

        # sm_policy_data['policy']['pccRules'] = {
        #     "PccRuleId-1": {
        #         "flowInfos": [
        #             {
        #                 "flowDescription": "permit out ip from any to assigned",
        #                 "flowDirection": "DOWNLINK"
        #             }
        #         ],
        #         "pccRuleId": "PccRuleId-1",
        #         "precedence": 100,
        #         "refQosData": [
        #             "2"
        #         ],
        #         "refChgData": [
        #             "ChgId-1"
        #         ]
        #     }
        # }

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
                        "precedence": "100",
                        "refQosData": "20"
                    }
                },
                "qosDecs": {
                    "20": {
                        "qosId": "20",
                        "5qi": "3",
                        "maxbrUl": "10 Mbps",
                        "maxbrDl": "10 Mbps",
                        "gbrUl": "0 Mbps",
                        "gbrDl": "0 Mbps"
                    }
                }
            }
        }


        # with open('./smpolicy_to_update.json', 'w') as json_file:
        #     json.dump(sm_policy_data, json_file, indent=4)



        print("_______________________________________________________________________________________")

        update_SmPolicy_by_id(sm_policy_id=sm_policy_id, sm_policy_data=post_data)

        print("__________________________Updated Policy data______________________________________________________")
        #print("Re Print data to check the changes")m_policy_data['policy']['sessRules']['SessRuleId-1']['authSessAmbr']

        re_status, sm_policy_data = get_SmPolicy_by_id(sm_policy_id)

        if (re_status):
            print(json.dumps(sm_policy_data["policy"], indent=4))




