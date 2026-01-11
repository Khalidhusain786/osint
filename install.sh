#!/bin/bash
# Khalid Husain - Ultimate Database Linker
echo -e "\e[1;32m[*] Fixing Scylla & Linking Deep Data Bots...\e[0m"

# 1. Clear locks (Screenshot 19:25 fix)
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm -rf /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock

# 2. Scylla & OSINT Dependencies (Manual Fix for Screenshot 20:31)
pip install colorama requests phonenumbers yagmail fpdf holehe maigret --break-system-packages --ignore-installed
pip install beautifulsoup4 lxml social-analyzer --break-system-packages

# 3. Scylla Re-cloning (Bypassing missing files)
mkdir -p tools
cd tools
rm -rf Scylla
git clone --depth=1 https://github.com/cybersecurity-team/Scylla.git
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] DEEP SEARCH ENGINE READY! Run: python3 khalid-osint.py\e[0m"
