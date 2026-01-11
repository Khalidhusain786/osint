cat << 'EOF' > install.sh
#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# System: Kali Linux / Ubuntu

echo -e "\e[1;32m[*] Installing Khalid-OSINT-Pro Dependencies...\e[0m"

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip git curl docker.io snapd xvfb xpdf poppler-utils

# Directories
mkdir -p reports

# Core OSINT Tools
echo "[*] Installing Holehe, Maigret, Sherlock, HIBP..."
pip3 install maigret holehe haveibeenpwned photon-cli colorama requests

# Sherlock Setup
git clone https://github.com/sherlock-project/sherlock.git ~/sherlock
cd ~/sherlock && pip3 install -r requirements.txt && cd -

# Amass Setup
sudo snap install amass

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] Setup Complete by Khalid Husain. Run: python3 khalid-osint.py\e[0m"
EOF
