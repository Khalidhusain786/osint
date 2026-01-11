#!/bin/bash
# Khalid Husain - Global Deep-Scan Final
echo -e "\e[1;32m[*] Cleaning and Installing Final Infrastructure...\e[0m"

# Clean system locks
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm -rf /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a

# Install only stable core modules
pip install colorama requests[socks] holehe maigret social-analyzer --break-system-packages --ignore-installed

# Start TOR for Dark Web access
sudo apt update && sudo apt install tor proxychains4 -y
sudo service tor start

echo -e "\e[1;34m[!] ALL SYSTEMS READY! Run: python3 khalid-osint.py\e[0m"
