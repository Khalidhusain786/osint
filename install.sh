#!/bin/bash
echo -e "\e[1;32m[*] Khalid-OSINT Master Setup Shuru...\e[0m"

# 1. System Dependencies
sudo apt update && sudo apt install tor proxychains4 python3-pip curl git exiftool nodejs npm googler -y

# 2. Python Tools (Telegram, Social, Email)
pip install colorama requests[socks] telethon holehe maigret sherlock socialscan --break-system-packages

# 3. Heavy Engines (Social Analyzer & PhoneInfoga)
sudo npm install -g social-analyzer
curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/install | bash
sudo mv ./phoneinfoga /usr/local/bin/

# 4. Finalizing
mkdir -p reports
sudo service tor restart
echo -e "\e[1;34m[!] Setup Complete. Ab 'python3 khalid-osint.py' chalayein.\e[0m"
