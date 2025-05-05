#it grab traffic at vxlan interface which is mirrored from upf
#It decodes the GTP header and forward this traffic to a new dummy interface dummy0

from scapy.all import *
from scapy.contrib.gtp import GTP_U_Header

def process_packet(packet):
    if packet.haslayer(GTP_U_Header):
        # Extract the GTP payload (should be an IP packet)
        inner_ip = packet[GTP_U_Header].payload

        # Ensure it's an IP packet
        if inner_ip.haslayer(IP):
            # Clone the packet to avoid modifying the original packet
            cloned_packet = inner_ip.copy()

            # Recalculate the IP checksum and correct the length fields
            del cloned_packet[IP].chksum
            del cloned_packet[IP].len
            cloned_packet = IP(bytes(cloned_packet[IP]))

            # Create a new Ethernet frame
            new_packet = Ether() / cloned_packet

            # Setting type might be redundant as Scapy should manage this for IP over Ethernet
            new_packet.type = 0x0800  # Type for IPv4

            # Send the reconstructed packet
            sendp(new_packet, iface="dummy0", verbose=False)

            # Print details for debugging
            #print(f"Sent IP packet from {cloned_packet.src} to {cloned_packet.dst} via dummy0")

def main():
    sniff(iface="vxlan0", prn=process_packet, filter="udp port 2152", store=False)

if __name__ == "__main__":
    main()
