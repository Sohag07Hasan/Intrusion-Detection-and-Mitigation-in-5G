#!/bin/bash

# Update package list
apt update

# Install Python 3 and pip
apt install -y python3 python3-pip python3-venv build-essential libatlas-base-dev

# Install packages from requirements.txt
pip3 install -r requirements.txt