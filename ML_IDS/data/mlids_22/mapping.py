import subprocess
import json

def send_curl_request(url, method):
    result = subprocess.run(['curl', '-X', method, url], capture_output=True, text=True)
    return result.stdout

def process_json_response(json_response):
    data = json.loads(json_response)
    #print(json_response) 
    processed_data = []
    for item in data:
        if item["PduSessions"] == None:
            continue
        processed_item = {
            'SmContext': [k["SmContextRef"] for k in item["PduSessions"]],
            'Supi': item.get('Supi')
        }
        #import pdb;pdb.set_trace()
        processed_data.append(processed_item)
    
    return processed_data

def write_to_text_file(supi, ip, cntxt, filename):
    # TODO: Instead of append, we need to check for any update in the existing file and add the new pdusessions info only
    with open(filename, 'a') as file:
        line = f"SmContext: {cntxt}\tip: {ip}\tSupi: {supi}\n"
        file.write(line)

if __name__ == "__main__":
    url = "http://amf.free5gc.org:8000/namf-oam/v1/registered-ue-context" 
    json_response = send_curl_request(url, "GET")
    processed_data = process_json_response(json_response)
    
    for ue in processed_data:
        supi = ue['Supi']
        for smcntxt in ue['SmContext']:
            url = "http://smf2.free5gc.org:8000/nsmf-oam/v1/ue-pdu-session-info/"+smcntxt
            json_response = send_curl_request(url, "GET")
            if json_response == "null":
                continue
            else:
                json_response = json.loads(json_response)
                ip = json_response["PDUAddress"]
            
            write_to_text_file(supi, ip, smcntxt, 'mapping_data.txt')
