#!/bin/bash

echo "[+] Starting Khalid Husain786 OSINT Environment Setup..."

# 1. Update system and install system-level dependencies for WeasyPrint/Python
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv \
    build-essential python3-dev python3-setuptools \
    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libpango1.0-dev \
    libjpeg-dev libopenjp2-7-dev libffi-dev \
    tor tor-geoipdb

# 2. Start TOR service (used by the script)
sudo service tor start

# 3. Install Python requirements
echo "[+] Installing Python modules..."
pip3 install --upgrade pip
pip3 install requests beautifulsoup4 colorama weasyprint pysocks

# 4. Check if the main script exists
if [ ! -f "khalid-osint.py" ]; then
    echo "[-] Error: khalid-osint.py not found in this folder!"
    exit 1
fi

# 5. Execution
echo "[+] Setup Complete. Launching OSINT tool..."
read -p "Enter Target (Email/Domain/Username): " target
python3 khalid-osint.py "$target"
