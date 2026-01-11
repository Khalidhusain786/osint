#!/bin/bash
# Khalid Husain - Global Deep Search Setup
echo -e "\e[1;32m[*] Installing Global 6-Layer Intelligence Framework...\e[0m"

# 1. Force Release System Locks
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm -rf /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a

# 2. Heavy-Duty Modules (No-Limit OSINT)
pip install colorama requests yagmail fpdf holehe maigret social-analyzer \
            shodan whois dnspython sublist3r python-whois --break-system-packages --ignore-installed

# 3. Directory Setup for Path-Tracking
mkdir -p reports/targets reports/infra reports/leaks

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] ALL LAYERS READY! Run: python3 khalid-osint.py\e[0m"
