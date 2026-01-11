#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Ultimate Force-Repair & Auto-Installer

echo -e "\e[1;32m[*] Khalid OSINT: Killing System Locks & Fixing Errors...\e[0m"

# 1. Force release all locks (Screenshot 19:25 ka fix)
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm /var/lib/apt/lists/lock /var/lib/dpkg/lock-frontend /var/cache/apt/archives/lock 2>/dev/null
sudo dpkg --configure -a

# 2. Setup folders
mkdir -p reports/txt tools modules

# 3. Fast Dependency Install (No System Upgrade)
sudo apt update -y
sudo apt install -y python3-pip python3-venv git curl --no-install-recommends

# 4. Global Modules Force Install (Screenshot 18:51 ka fix)
pip install colorama requests phonenumbers fpdf holehe maigret --break-system-packages --ignore-installed

# 5. Local Engines Setup
cd tools
git clone --depth=1 https://github.com/sherlock-project/sherlock.git 2>/dev/null || (cd sherlock && git pull)
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] ALL LOCKS CLEARED! Run: python3 khalid-osint.py\e[0m"
