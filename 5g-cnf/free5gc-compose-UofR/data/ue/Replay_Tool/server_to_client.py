from scapy.all import *
from threading import Thread
import sys
import random
import os
import time


class TrafficGenerator(Thread):
    def __init__(self, s_ip, d_ip, r_port, pcap_file, fragsize):
        Thread.__init__(self)
        self.s_ip = s_ip
        self.d_ip = d_ip
        self.r_port = r_port
        self.pcap_file = pcap_file
        self.fragsize = fragsize

    def run(self):
        start_time = time.time()
        self.send_packet(self.s_ip, self.d_ip, self.r_port, self.pcap_file, self.fragsize)
        end_time = time.time()
        print(f"Execution time for {self.pcap_file}: {end_time - start_time} seconds")

    def send_packet(self, s_ip, d_ip, r_port, pcap_file, fragsize):
        pkt_count = 0
        reader = PcapReader(pcap_file)
        #allowed_ports = [443, 80, 8080, 22, 20, 53, 67, 25]

        last_timestamp = None
        for pkt in reader:
            if IP in pkt: #and pkt[IP].dport not in allowed_ports:
                pkt_count += 1
                new_pkt = pkt.copy()
                new_pkt[IP].dst = d_ip
                new_pkt[IP].src = s_ip
                #new_pkt[IP].sport = int(r_port)
                #new_pkt[IP].dport = int(r_port)
                del new_pkt[IP].chksum
                if TCP in new_pkt:
                    del new_pkt[TCP].chksum
                elif UDP in new_pkt:
                    del new_pkt[UDP].chksum

                # if last_timestamp is not None: 
                #     delay = float(pkt.time) - float(last_timestamp)
                #     time.sleep(delay)
                # last_timestamp = pkt.time

                fragments = fragment(new_pkt, fragsize=fragsize)
                for frag in fragments:
                    send(frag, verbose=False)

        print(f"Total packets sent: {pkt_count}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python traffic_replay_frag.py config.txt")
        sys.exit(1)

    config_path = sys.argv[1]
    threads = [] #added later

    with open(config_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            # Unpack the parts with an optional fragsize
            if len(parts) == 5:
                s_ip, d_ip, r_port, traffic_type, fragsize_str = parts
                fragsize = int(fragsize_str)
            else:
                s_ip, d_ip, r_port, traffic_type = parts
                fragsize = 1500  # Default value

            pcap_dir = "../"
            pcap_files = os.listdir(os.path.join(pcap_dir, traffic_type))
            if not pcap_files:
                print(f"No pcap files found for traffic type '{traffic_type}'. Skipping...")
                continue

            for pcap_file in pcap_files:
                full_pcap_path = os.path.join(pcap_dir, traffic_type, pcap_file)
                traffic_generator = TrafficGenerator(s_ip, d_ip, r_port, full_pcap_path, fragsize)
                traffic_generator.start()
                threads.append(traffic_generator)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All traffic has been processed.")

            # ##### Uncomment this part to select random pcap file ######
            # pcap_file = random.choice(pcap_files)  #here is randomly selects any of the pcap from the selected directory
            # full_pcap_path = os.path.join(pcap_dir, traffic_type, pcap_file)
            #
            # traffic_generator = TrafficGenerator(s_ip, d_ip, r_port, full_pcap_path, fragsize)
            # traffic_generator.start()
            # traffic_generator.join()
