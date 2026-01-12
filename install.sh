#!/bin/bash
echo -e "\e[1;32m[*] Installing Khalid Global-OSINT Framework...\e[0m"

# 1. System & Tor Setup
sudo apt update && sudo apt install tor proxychains4 python3-pip curl git lynx googler -y
sudo service tor restart

# 2. Python Power-Tools
pip install colorama requests[socks] telethon holehe maigret sherlock socialscan instaloader --break-system-packages

# 3. Phone & Meta Tools
curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/install | bash
sudo mv ./phoneinfoga /usr/local/bin/

mkdir -p reports
echo -e "\e[1;34m[!] All layers (Surface, Deep, Dark) are ready.\e[0m"
