# Use the latest Ubuntu base image
FROM ubuntu:latest

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Update apt and install software-properties-common to manage PPAs
RUN apt-get update && apt-get install -y software-properties-common

# Add the Suricata PPA
RUN add-apt-repository ppa:oisf/suricata-stable

# Update apt sources and install Suricata
RUN apt-get update && apt-get install -y suricata

# Clean up to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose ports (if needed, e.g., for syslog, JSON output)
EXPOSE 4500/udp 514/udp

# Set default CMD
#CMD ["suricata", "-c", "/etc/suricata/suricata.yaml", "-i", "eth0"]
