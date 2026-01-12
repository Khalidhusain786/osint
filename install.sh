#!/bin/bash
echo -e "\e[1;32m[*] Khalid-OSINT Master Setup Shuru Ho Raha Hai...\e[0m"

# System updates aur essential tools
sudo apt update && sudo apt install tor proxychains4 python3-pip curl git exiftool nodejs npm googler -y

# Telegram aur OSINT Libraries
pip install colorama requests[socks] telethon holehe maigret sherlock socialscan instaloader --break-system-packages

# Social-Analyzer aur PhoneInfoga Setup
sudo npm install -g social-analyzer
curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/install | bash
sudo mv ./phoneinfoga /usr/local/bin/

# Directory aur Services
mkdir -p reports
sudo service tor restart

echo -e "\e[1;34m[!] Setup Complete! Ab bas 'python3 khalid-osint.py' chalayein.\e[0m"
