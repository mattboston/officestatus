#!/bin/bash

# Install the required dependencies
sudo apt-get install python3-pip python3-dev python3-venv

# Create a python virtual environment
sudo python3 -m venv .venv

# Activate the python virtual environment
sudo source .venv/bin/activate

# Install the pip modules
sudo pip3 install -r ./requirements.txt

# Install the officestatus systemd service file
sudo cp officestatus.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload
