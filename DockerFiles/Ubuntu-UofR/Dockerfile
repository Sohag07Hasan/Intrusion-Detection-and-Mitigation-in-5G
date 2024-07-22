# Use the official Ubuntu image as the base
FROM ubuntu:latest

# Optional: Set a maintainer or label for the image
LABEL maintainer="uofr"

# Avoid prompts from apt
ARG DEBIAN_FRONTEND=noninteractive

# Update package lists and install software
RUN apt-get update && \
    apt-get install -y \
    # Add the packages you need, for example:
    curl \
    vim \
    iperf3 \
    tcpdump \
    iproute2 \
    iputils-ping \
    nmap \
    # Add any other packages you need here
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Optional: Copy files or directories from the host into the container
# COPY <src> <dest>
# For example, to copy a script from the host to the container:
# COPY ./myscript.sh /usr/local/bin/myscript.sh

# Optional: Set working directory
# WORKDIR /path/to/workdir

# Optional: Expose ports (if your application uses any)
# EXPOSE <port>
# For example, to expose port 80 for a web server:
EXPOSE 5000
EXPOSE 80
EXPOSE 8080
EXPOSE 443

# Specify the command to run when the container starts
# Here you can use CMD or ENTRYPOINT depending on your needs
CMD ["bash"]
