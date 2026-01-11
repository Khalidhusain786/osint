#!/bin/bash
# Khalid Husain - Global Deep-Scan Setup (No-Limit Version)

echo -e "\e[1;32m[*] Telegram Bot Mirror & Breach Data Setup Shuru...\e[0m"

# 1. System Cleanup & TOR Setup
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm -rf /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo apt update
sudo apt install tor proxychains4 python3-pip -y
sudo service tor start

# 2. Telegram Bot Style Searching Tools
pip install colorama requests[socks] holehe maigret social-analyzer --break-system-packages --ignore-installed

# 3. Path Fix
mkdir -p /root/osint/reports
echo -e "\e[1;34m[!] Setup Done! Ab python3 khalid-osint.py chalayein.\e[0m"
