#!/bin/bash
# Khalid Husain - Telegram Bot Style Master Setup
echo -e "\e[1;32m[*] Breaking locks and merging all OSINT tools...\e[0m"

# 1. Force System Repair (Lock Fix)
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm -rf /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a

# 2. Manual Dependency Install (No Missing Errors)
pip install colorama requests phonenumbers yagmail fpdf holehe maigret beautifulsoup4 lxml social-analyzer --break-system-packages --ignore-installed

# 3. Scylla & Breach Tool Setup
mkdir -p tools
cd tools
rm -rf Scylla # Purana delete
git clone --depth=1 https://github.com/cybersecurity-team/Scylla.git 2>/dev/null
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] ALL TOOLS MERGED! Run: python3 khalid-osint.py\e[0m"
