#!/bin/bash
# Khalid Husain - Hybrid Stealth OSINT v5.0
echo -e "\e[1;32m[*] Setting up Hybrid Engine & Stealth (MAC Spoofer)...\e[0m"

# 1. System Repair & Tools
sudo apt update && sudo apt install tor macchanger proxychains4 -y
sudo service tor start

# 2. Python Hybrid Modules
pip install colorama requests[socks] yagmail fpdf holehe maigret \
            googletrans==4.0.0-rc1 social-analyzer --break-system-packages --ignore-installed

# 3. Security (MAC Spoofing)
sudo macchanger -r eth0 2>/dev/null
sudo macchanger -r wlan0 2>/dev/null

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] STEALTH HYBRID ENGINE READY! Run: python3 khalid-osint.py\e[0m"
