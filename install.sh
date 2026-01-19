#!/bin/bash

# 1. Fix Broken Dependencies
echo "Attempting to fix broken packages..."
sudo apt update
sudo apt --fix-broken install -y

# 2. Install Python Core & Build Essentials (Required for many OSINT tools)
echo "Installing core dependencies..."
sudo apt install python3 python3-pip python3-venv python3-full build-essential libssl-dev libffi-dev -y

# 3. Handle the 'tor.service' if missing
echo "Checking Tor service..."
if ! systemctl list-unit-files | grep -q tor.service; then
    sudo apt install tor -y
fi
sudo systemctl enable tor
sudo systemctl start tor

# 4. Create a Virtual Environment to avoid System-Level Conflicts
echo "Setting up Python Virtual Environment..."
python3 -m venv osint_env
source osint_env/bin/activate

# 5. Install Python Requirements
echo "Installing Python modules..."
pip install requests colorama

echo "------------------------------------------------"
echo "Setup Complete. To run your script, use:"
echo "source osint_env/bin/activate"
echo "python3 khalid-osint-v90.py <target>"
echo "------------------------------------------------"
