#!/bin/bash
echo -e "\e[1;32m[*] Installing Khalid Deep-Data OSINT Framework...\e[0m"

# Basic Tools
sudo apt update && sudo apt install tor proxychains4 python3-pip -y

# Libraries
pip install colorama requests[socks] telethon holehe maigret --break-system-packages

# Tools
curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/install | bash
sudo mv ./phoneinfoga /usr/local/bin/

mkdir -p reports
echo -e "\e[1;34m[!] Setup Ready. 'khalid_session' create hoga run karne par.\e[0m"
