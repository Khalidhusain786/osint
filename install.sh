#!/bin/bash
echo -e "\e[1;32m[*] Installing Khalid All-in-One OSINT Framework...\e[0m"

# 1. Install Networking & Tor
sudo apt update
sudo apt install tor proxychains4 whois dnsutils python3-pip -y

# 2. Configure Proxychains (Silent Setup)
sudo sed -i 's/strict_chain/#strict_chain/' /etc/proxychains4.conf
sudo sed -i 's/#dynamic_chain/dynamic_chain/' /etc/proxychains4.conf

# 3. Start Tor Service
sudo service tor restart

# 4. Install OSINT Engines
pip install colorama requests[socks] holehe maigret social-analyzer --break-system-packages --ignore-installed

mkdir -p /root/osint/reports
echo -e "\e[1;34m[!] Setup Complete! Tor Service is now running in background.\e[0m"
